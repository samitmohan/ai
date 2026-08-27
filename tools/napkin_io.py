#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.11"
# ///
"""Measures the two levels below DRAM on this machine: the SSD and the network.

    uv run tools/napkin_io.py

SSD numbers use fcntl F_NOCACHE so the page cache cannot answer the read. The
test file is written to the scratchpad and deleted afterwards. Network numbers
are TCP handshake time to AWS regional endpoints, which is exactly one round
trip, so they include queueing and routing rather than pure propagation delay.
"""

from __future__ import annotations

import fcntl
import os
import random
import socket
import statistics
import subprocess
import sys
import tempfile
import time

F_NOCACHE = 48
FILE_BYTES = 2 << 30
BLOCK = 4096


def make_file(path: str) -> None:
    chunk = os.urandom(1 << 20)
    with open(path, "wb") as f:
        for _ in range(FILE_BYTES >> 20):
            f.write(chunk)
        f.flush()
        os.fsync(f.fileno())
    subprocess.run(["sync"], check=False)


def open_uncached(path: str) -> int:
    fd = os.open(path, os.O_RDONLY)
    fcntl.fcntl(fd, F_NOCACHE, 1)
    return fd


def random_read_us(path: str, n: int, block: int) -> tuple[float, float]:
    fd = open_uncached(path)
    max_off = (FILE_BYTES - block) // block
    offs = [random.randrange(max_off) * block for _ in range(n)]
    samples = []
    try:
        for off in offs:
            t0 = time.perf_counter_ns()
            os.pread(fd, block, off)
            samples.append(time.perf_counter_ns() - t0)
    finally:
        os.close(fd)
    samples.sort()
    return statistics.median(samples) / 1e3, samples[int(n * 0.99)] / 1e3


def seq_read_gbs(path: str, block: int) -> float:
    fd = open_uncached(path)
    total = 0
    t0 = time.perf_counter()
    try:
        while True:
            b = os.read(fd, block)
            if not b:
                break
            total += len(b)
    finally:
        os.close(fd)
    return total / (time.perf_counter() - t0) / 1e9


def seq_write_gbs(path: str, block: int, nblocks: int, fsync_every: int | None) -> float:
    buf = os.urandom(block)
    fd = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_TRUNC)
    fcntl.fcntl(fd, F_NOCACHE, 1)
    t0 = time.perf_counter()
    try:
        for i in range(nblocks):
            os.write(fd, buf)
            if fsync_every and (i + 1) % fsync_every == 0:
                os.fsync(fd)
        if not fsync_every:
            os.fsync(fd)
    finally:
        os.close(fd)
    return block * nblocks / (time.perf_counter() - t0) / 1e9


def tcp_rtt_ms(host: str, port: int = 443, n: int = 7) -> tuple[str, float] | None:
    try:
        ip = socket.gethostbyname(host)
    except OSError:
        return None
    samples = []
    for _ in range(n):
        s = socket.socket()
        s.settimeout(5)
        t0 = time.perf_counter()
        try:
            s.connect((ip, port))
        except OSError:
            s.close()
            continue
        samples.append((time.perf_counter() - t0) * 1e3)
        s.close()
    if not samples:
        return None
    return ip, min(samples)


REGIONS = [
    ("ap-south-1", "Mumbai", "ec2.ap-south-1.amazonaws.com"),
    ("ap-southeast-1", "Singapore", "ec2.ap-southeast-1.amazonaws.com"),
    ("ap-northeast-1", "Tokyo", "ec2.ap-northeast-1.amazonaws.com"),
    ("eu-west-1", "Ireland", "ec2.eu-west-1.amazonaws.com"),
    ("eu-central-1", "Frankfurt", "ec2.eu-central-1.amazonaws.com"),
    ("us-east-1", "N. Virginia", "ec2.us-east-1.amazonaws.com"),
    ("us-west-1", "N. California", "ec2.us-west-1.amazonaws.com"),
    ("sa-east-1", "Sao Paulo", "ec2.sa-east-1.amazonaws.com"),
]

FIBRE_KM_PER_S = 204_000  # c / 1.47, the refractive index of single-mode fibre


def main() -> int:
    tmp = os.environ.get("NAPKIN_TMP") or tempfile.gettempdir()
    path = os.path.join(tmp, "napkin_io.bin")

    print(f"SSD, {FILE_BYTES >> 30} GiB file at {path}, F_NOCACHE, "
          f"page cache bypassed")
    make_file(path)
    for block in (4096, 8192, 131072):
        med, p99 = random_read_us(path, 2000, block)
        print(f"  random read  {block // 1024:4d} KiB   median {med:8.1f} us   "
              f"p99 {p99:8.1f} us   {block / med * 1e6 / 1e6:6.0f} MB/s at QD1")
    print(f"  sequential read, 1 MiB blocks       {seq_read_gbs(path, 1 << 20):6.2f} GB/s")
    print(f"  sequential write, 1 MiB, fsync once {seq_write_gbs(path, 1 << 20, 512, None):6.2f} GB/s")
    print(f"  sequential write, 8 KiB, fsync each {seq_write_gbs(path, 8192, 2000, 1) * 1e3:6.1f} MB/s")
    os.unlink(path)

    print("\nnetwork, TCP handshake to AWS regional endpoints, one round trip, "
          "best of 7")
    for code, city, host in REGIONS:
        r = tcp_rtt_ms(host, n=7)
        if r is None:
            print(f"  {city:<14} {code:<16} unreachable")
            continue
        ip, ms = r
        km = ms / 1e3 / 2 * FIBRE_KM_PER_S
        print(f"  {city:<14} {code:<16} {ms:7.1f} ms   implies <= "
              f"{km:6.0f} km of fibre one way")
    return 0


if __name__ == "__main__":
    sys.exit(main())
