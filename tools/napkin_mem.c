// Measures the memory hierarchy on this machine: cycle time, cache/DRAM load
// latency, and sequential read bandwidth. No vendor specs, no constants.
//
//   cc -O2 -o /tmp/napkin_mem tools/napkin_mem.c && /tmp/napkin_mem
//
// Latency comes from a pointer chase around one random cycle of cache lines, so
// every load depends on the previous one and no prefetcher can hide it. The
// cycle time comes from a chain of dependent integer adds, which retire one per
// cycle, so ns/add is the clock period. Cache latencies are then reported in
// cycles without asking the vendor what the clock is.

#include <pthread.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>
#include <pthread/qos.h>
#include <unistd.h>
#include <errno.h>

#define LINE 128   // sysctl hw.cachelinesize on Apple silicon

static double now_s(void) {
  struct timespec t;
  clock_gettime(CLOCK_MONOTONIC, &t);
  return t.tv_sec + t.tv_nsec * 1e-9;
}

// One dependent add per iteration of the unrolled body. Integer add latency is
// one cycle on every core worth measuring, so this yields the clock period.
static double cycle_ns(void) {
  const long n = 200000000L;
  uint64_t x = 1;
  double t0 = now_s();
  for (long i = 0; i < n / 10; i++) {
    __asm__ volatile("add %0, %0, #1" : "+r"(x));
    __asm__ volatile("add %0, %0, #1" : "+r"(x));
    __asm__ volatile("add %0, %0, #1" : "+r"(x));
    __asm__ volatile("add %0, %0, #1" : "+r"(x));
    __asm__ volatile("add %0, %0, #1" : "+r"(x));
    __asm__ volatile("add %0, %0, #1" : "+r"(x));
    __asm__ volatile("add %0, %0, #1" : "+r"(x));
    __asm__ volatile("add %0, %0, #1" : "+r"(x));
    __asm__ volatile("add %0, %0, #1" : "+r"(x));
    __asm__ volatile("add %0, %0, #1" : "+r"(x));
  }
  double dt = now_s() - t0;
  if (x == 0) printf("unreachable\n");
  return dt / n * 1e9;
}

// Eight independent chains, so the core can retire several adds per cycle. The
// gap between this and cycle_ns is the width of the machine.
static double add_throughput_ns(void) {
  const long n = 400000000L;
  uint64_t a = 1, b = 2, c = 3, d = 4, e = 5, f = 6, g = 7, h = 8;
  double t0 = now_s();
  for (long i = 0; i < n / 8; i++) {
    __asm__ volatile("add %0, %0, #1" : "+r"(a));
    __asm__ volatile("add %0, %0, #1" : "+r"(b));
    __asm__ volatile("add %0, %0, #1" : "+r"(c));
    __asm__ volatile("add %0, %0, #1" : "+r"(d));
    __asm__ volatile("add %0, %0, #1" : "+r"(e));
    __asm__ volatile("add %0, %0, #1" : "+r"(f));
    __asm__ volatile("add %0, %0, #1" : "+r"(g));
    __asm__ volatile("add %0, %0, #1" : "+r"(h));
  }
  double dt = now_s() - t0;
  if (a + b + c + d + e + f + g + h == 0) printf("unreachable\n");
  return dt / n * 1e9;
}

static uint32_t *chase_build(size_t bytes, size_t *out_lines) {
  size_t lines = bytes / LINE;
  if (lines < 2) lines = 2;
  size_t alloc = (lines * LINE + 4095) / 4096 * 4096;
  uint32_t *buf = aligned_alloc(4096, alloc);
  if (!buf) { perror("aligned_alloc"); exit(1); }
  memset(buf, 0, alloc);

  // Fisher-Yates a permutation, then thread it into a single cycle so the walk
  // touches every line exactly once before repeating.
  uint32_t *perm = malloc(lines * sizeof(uint32_t));
  for (size_t i = 0; i < lines; i++) perm[i] = (uint32_t)i;
  for (size_t i = lines - 1; i > 0; i--) {
    size_t j = (size_t)(random() % (long)(i + 1));
    uint32_t t = perm[i]; perm[i] = perm[j]; perm[j] = t;
  }
  for (size_t i = 0; i < lines; i++) {
    size_t from = perm[i], to = perm[(i + 1) % lines];
    buf[from * (LINE / 4)] = (uint32_t)(to * (LINE / 4));
  }
  free(perm);
  *out_lines = lines;
  return buf;
}

static double chase_ns(size_t bytes, long steps) {
  size_t lines;
  uint32_t *buf = chase_build(bytes, &lines);
  uint32_t idx = 0;
  for (long i = 0; i < 200000; i++) idx = buf[idx];   // warm TLB and caches
  double t0 = now_s();
  for (long i = 0; i < steps; i++) idx = buf[idx];
  double dt = now_s() - t0;
  if (idx == 0xffffffff) printf("unreachable\n");
  free(buf);
  return dt / steps * 1e9;
}

// One cache line per page, walked in random page order, at a RANDOM offset inside
// each page. The random offset is load-bearing: picking offset 0 in every page
// makes every address share the same cache set-index bits, so a page-size stride
// thrashes a few hundred lines of L2 and the result reads like a DRAM miss with no
// TLB involved at all. With the offset spread, the touched bytes stay small enough
// to live in L2 and the only thing growing with npages is the number of live
// address translations, so any jump prices a page walk.
static double tlb_ns(size_t npages, long steps, int spread) {
  size_t ps = (size_t)getpagesize();
  size_t words = ps / sizeof(uint32_t);
  uint32_t *buf = aligned_alloc(ps, npages * ps);
  if (!buf) { perror("aligned_alloc"); exit(1); }
  memset(buf, 0, npages * ps);

  size_t lines_per_page = ps / LINE;
  uint32_t *perm = malloc(npages * sizeof(uint32_t));
  uint32_t *slot = malloc(npages * sizeof(uint32_t));
  for (size_t i = 0; i < npages; i++) {
    perm[i] = (uint32_t)i;
    slot[i] = spread ? (uint32_t)(random() % (long)lines_per_page) : 0;
  }
  for (size_t i = npages - 1; i > 0; i--) {
    size_t j = (size_t)(random() % (long)(i + 1));
    uint32_t t = perm[i]; perm[i] = perm[j]; perm[j] = t;
  }
  uint32_t start = 0;
  for (size_t i = 0; i < npages; i++) {
    size_t from = (size_t)perm[i], to = (size_t)perm[(i + 1) % npages];
    uint32_t here = (uint32_t)(from * words + slot[from] * (LINE / 4));
    if (i == 0) start = here;
    buf[here] = (uint32_t)(to * words + slot[to] * (LINE / 4));
  }
  free(perm);
  free(slot);

  uint32_t idx = start;
  for (long i = 0; i < 200000; i++) idx = buf[idx];
  double t0 = now_s();
  for (long i = 0; i < steps; i++) idx = buf[idx];
  double dt = now_s() - t0;
  if (idx == 0xffffffff) printf("unreachable\n");
  free(buf);
  return dt / steps * 1e9;
}

// Read-only streaming sum. Four accumulators so the adds are not the bottleneck.
static double seq_read_gbs(size_t bytes, int reps) {
  size_t n = bytes / sizeof(uint64_t);
  uint64_t *buf = aligned_alloc(4096, n * sizeof(uint64_t));
  if (!buf) { perror("aligned_alloc"); exit(1); }
  for (size_t i = 0; i < n; i++) buf[i] = i;
  uint64_t s0 = 0, s1 = 0, s2 = 0, s3 = 0;
  for (size_t i = 0; i < n; i += 4) { s0 += buf[i]; }        // warm
  double t0 = now_s();
  for (int r = 0; r < reps; r++)
    for (size_t i = 0; i + 3 < n; i += 4) {
      s0 += buf[i]; s1 += buf[i + 1]; s2 += buf[i + 2]; s3 += buf[i + 3];
    }
  double dt = now_s() - t0;
  if (s0 + s1 + s2 + s3 == 0) printf("unreachable\n");
  free(buf);
  return (double)bytes * reps / dt / 1e9;
}

static double best(double (*f)(void), int k) {
  double m = 1e18;
  for (int i = 0; i < k; i++) { double v = f(); if (v < m) m = v; }
  return m;
}

static double best_chase(size_t bytes, long steps, int k) {
  double m = 1e18;
  for (int i = 0; i < k; i++) { double v = chase_ns(bytes, steps); if (v < m) m = v; }
  return m;
}

// A syscall that always fails, so nothing but the user/kernel transition is timed.
static double syscall_ns(void) {
  const long n = 2000000L;
  double t0 = now_s();
  for (long i = 0; i < n; i++) close(-1);
  return (now_s() - t0) / n * 1e9;
}

struct band_arg { uint64_t *buf; size_t n; int reps; uint64_t sink; };

static void *band_worker(void *p) {
  struct band_arg *a = p;
  uint64_t s0 = 0, s1 = 0, s2 = 0, s3 = 0;
  for (int r = 0; r < a->reps; r++)
    for (size_t i = 0; i + 3 < a->n; i += 4) {
      s0 += a->buf[i]; s1 += a->buf[i + 1];
      s2 += a->buf[i + 2]; s3 += a->buf[i + 3];
    }
  a->sink = s0 + s1 + s2 + s3;
  return NULL;
}

// Each thread streams its own slice, so this finds the DRAM ceiling rather than
// the per-core load/store limit.
static double seq_read_threaded_gbs(size_t bytes, int reps, int nthreads) {
  size_t n = bytes / sizeof(uint64_t);
  uint64_t *buf = aligned_alloc(4096, n * sizeof(uint64_t));
  if (!buf) { perror("aligned_alloc"); exit(1); }
  for (size_t i = 0; i < n; i++) buf[i] = i;
  pthread_t th[64];
  struct band_arg args[64];
  size_t per = n / nthreads;
  double t0 = now_s();
  for (int t = 0; t < nthreads; t++) {
    args[t] = (struct band_arg){buf + t * per, per, reps, 0};
    pthread_create(&th[t], NULL, band_worker, &args[t]);
  }
  for (int t = 0; t < nthreads; t++) pthread_join(th[t], NULL);
  double dt = now_s() - t0;
  uint64_t sink = 0;
  for (int t = 0; t < nthreads; t++) sink += args[t].sink;
  if (sink == 0) printf("unreachable\n");
  free(buf);
  return (double)(per * sizeof(uint64_t) * nthreads) * reps / dt / 1e9;
}

int main(void) {
  pthread_set_qos_class_self_np(QOS_CLASS_USER_INTERACTIVE, 0);
  srandom(12345);

  (void)add_throughput_ns();                 // let the scheduler promote us to a P-core
  double cyc = best(cycle_ns, 5);
  double thr = best(add_throughput_ns, 3);
  printf("dependent integer add   %8.3f ns   (= clock period, %.2f GHz)\n",
         cyc, 1.0 / cyc);
  printf("independent integer add %8.3f ns   (%.1f adds retired per cycle)\n\n",
         thr, cyc / thr);

  size_t sizes[] = {
      4ull << 10, 16ull << 10, 32ull << 10, 64ull << 10, 128ull << 10,
      256ull << 10, 512ull << 10, 1ull << 20, 2ull << 20, 4ull << 20,
      8ull << 20, 16ull << 20, 32ull << 20, 64ull << 20, 128ull << 20,
      256ull << 20, 512ull << 20, 1024ull << 20};
  printf("%12s %12s %10s\n", "working set", "load latency", "cycles");
  for (size_t i = 0; i < sizeof(sizes) / sizeof(sizes[0]); i++) {
    long steps = sizes[i] <= (8ull << 20) ? 30000000L : 5000000L;
    double ns = best_chase(sizes[i], steps, 3);
    if (sizes[i] >= (1ull << 20))
      printf("%9zu MiB %9.2f ns %10.1f\n", sizes[i] >> 20, ns, ns / cyc);
    else
      printf("%9zu KiB %9.2f ns %10.1f\n", sizes[i] >> 10, ns, ns / cyc);
  }

  printf("\none line per page, so only the translation count grows\n");
  printf("%11s %10s %14s %8s %14s\n", "pages live", "footprint",
         "spread offset", "cycles", "offset 0");
  size_t np[] = {16, 64, 256, 1024, 2048, 3072, 4096, 8192, 16384, 32768, 65536};
  for (size_t i = 0; i < sizeof(np) / sizeof(np[0]); i++) {
    double sp = 1e18, z = 1e18;
    for (int k = 0; k < 3; k++) {
      double v = tlb_ns(np[i], 5000000L, 1);
      if (v < sp) sp = v;
      double w = tlb_ns(np[i], 5000000L, 0);
      if (w < z) z = w;
    }
    printf("%11zu %7zu KiB %11.2f ns %8.1f %11.2f ns\n", np[i],
           np[i] * (size_t)LINE / 1024, sp, sp / cyc, z);
  }

  printf("\nsequential read, 512 MiB working set\n");
  printf("%12s %12s\n", "threads", "GB/s");
  printf("%12d %12.1f\n", 1, seq_read_gbs(512ull << 20, 4));
  for (int t = 2; t <= 10; t += 2)
    printf("%12d %12.1f\n", t, seq_read_threaded_gbs(512ull << 20, 4, t));

  printf("\nfailing syscall (close(-1)): %.0f ns\n", best(syscall_ns, 3));
  return 0;
}
