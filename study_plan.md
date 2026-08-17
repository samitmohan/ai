# Study Plan (Ordered)

Gate out of each phase before starting the next.

---

## Phase 0: Unblock (2-3 weeks)

CS336's stated prerequisites, nothing more.

- [Essential Math](https://alisawuffles.notion.site/math-notes#3737eb87360580b3b555e3c616713286) - only the rusty parts: linalg, probability, matrix calculus, napkin math
- [Karpathy Zero to Hero] - all 8 videos, typed by hand in a blank file
- Docker basics - 3 hours: build, run, `-v`, `--gpus all`. Full guide deferred to Phase 4
- Papers, after nanoGPT runs:
  - [Understanding LSTM Networks](https://colah.github.io/posts/2015-08-Understanding-LSTMs/)
  - [Attention Is All You Need](https://arxiv.org/abs/1706.03762)
  - [AlexNet](https://papers.nips.cc/paper/2012/hash/c399862d3b9d6b76c8436e924a68c45b-Abstract.html) - skim
  - [Deep Residual Learning (ResNet)](https://arxiv.org/abs/1512.03385) - skim

Deferred out of this phase: CUDA book (Phase 2), FastAPI/threading (Phase 4), CNN playlist (Phase 6).

**Gate:** nanoGPT trains, written from understanding rather than transcription.

---

## Phase 1: Build the transformer until it's boring (4-6 weeks)

- [Building LLMs from Scratch] (Raschka) - second pass on purpose; adds real GPT-2 weight loading and task heads
- [Life of a Token](https://www.aleksagordic.com/blog/transforme) - best whole-stack mental model available
- Karpathy "Let's reproduce GPT-2 (124M)"
- Karpathy **nanochat** - addition to the original plan: pretrain -> SFT -> RL -> chat UI in one repo. Gives the shape of the full pipeline before CS336 makes you build each piece properly
- Architecture deltas (RoPE, RMSNorm, GQA, SwiGLU):
  - [Language Models are Few-Shot Learners (GPT-3)](https://arxiv.org/abs/2005.14165)
  - [LLaMA 2](https://arxiv.org/abs/2307.09288)
  - [Mistral 7B](https://arxiv.org/abs/2310.06825)
  - [Raschka LLM Architecture Gallery](https://sebastianraschka.com/llm-architecture-gallery/) - companion diff-viewer, not a linear read
- [Notes on essential LLM](https://alisawuffles.notion.site/alisa-s-book-of-llms) - reference, keep open
- MiniTorch code walkthrough; read tinygrad (geohot) and blog on making your own pytorch (minitorch redo)

**Gate:** [GPT-2 from an empty file, no reference, under an hour, and it trains](https://www.youtube.com/watch?v=xmkSf5IS-zw&t=1636s). Repeat until true. Do not start Phase 2 before passing.

---

## Phase 2: CS336, all five assignments (8-12 weeks)

[CS336 Spring 2025](https://cs336.stanford.edu/spring2025/) - the bulk of the year.

### A1: Basics (tokenizer, architecture, optimizer, training)
No companion reading. Phase 1 was the prep.

### A2: Systems (profiling, Triton FlashAttention2, distributed training)
Companion reading, in order:
- [Memory (drepper, cpumemory)](https://akkadia.org/drepper/cpumemory.pdf) - memory hierarchy chapters
- [CUDA for Deep Learning](https://www.manning.com/books/cuda-for-deep-learning) (Alredge) - arrives here, with a slow kernel in front of you
- [FlashAttention](https://arxiv.org/abs/2205.14135) - v1, deep
- [FlashAttention 1-4](https://arxiv.org/pdf/2603.05451) - skim for deltas only
- [ThunderKittens](https://arxiv.org/pdf/2410.20399)
- [GPipe](https://arxiv.org/abs/1811.06965) - during the parallelism lectures

### A3: Scaling (scaling-law fitting)
- [Thinking in JAX](https://docs.jax.dev/en/latest/notebooks/thinking_in_jax.html) - one day
- [How to Scale Your Model](https://jax-ml.github.io/scaling-book/) - exercises handwritten. Ch.1 roofline and ch.4 transformer math are the highest-value pages in the whole plan
- [Scaling Laws for Neural Language Models](https://arxiv.org/abs/2001.08361)
- [Training Compute-Optimal LLMs (Chinchilla)](https://arxiv.org/abs/2203.15556)

### A4: Data (CommonCrawl filtering, dedup)
No companion reading.

### A5: Alignment and Reasoning RL (SFT + RL for math)
- [Training LLMs to Follow Instructions (InstructGPT)](https://arxiv.org/abs/2203.02155)
- [Direct Preference Optimization (DPO)](https://arxiv.org/abs/2305.18290)
- [Constitutional AI](https://arxiv.org/abs/2212.08073)
- [Build DeepSeek](https://www.youtube.com/playlist?list=PLPTV0NXA_ZSiOpKKlHCyOq9lnp-dLvlms) + [DeepSeek-V2](https://arxiv.org/abs/2405.04434) - MLA and MoE, back-fills the MoE lecture
- [Building a reasoning model]

**Gate:** a Triton attention kernel that beats the naive version, with measured wall-clock and achieved bandwidth.

---

## Phase 3: Fine-tuning, hands on hardware (3-4 weeks)

- [Fine Tuning LLMs](https://magazine.sebastianraschka.com/p/finetuning-large-language-models)
- [Fine Tuning on single GPU (grad accumulation)](https://sebastianraschka.com/blog/2023/llm-grad-accumulation.html)
- [PEFT / adapters](https://sebastianraschka.com/blog/2023/llm-finetuning-llama-adapter.html)
- [LoRA](https://sebastianraschka.com/blog/2023/llm-finetuning-lora.html)
- [Fine tuning pretrained transformers](https://magazine.sebastianraschka.com/p/using-and-finetuning-pretrained-transformers)

Then papers: [LoRA](https://arxiv.org/abs/2106.09685), [QLoRA](https://arxiv.org/abs/2305.14314).

Then hardware: [Unsloth Fine Tuning] on bqa1/bqa3.

Case study to imitate: [Teaching a tiny model to prove hard theorems (qed-nano)](https://huggingface.co/spaces/lm-provers/qed-nano-blogpost).

Checklist at the end, not a textbook: [LLM Fine Tuning Interview Handbook].

**Gate:** a fine-tuned model on a task you chose, with an eval harness and a writeup of what failed.

---

## Phase 4: Inference and the engineering layer (4-6 weeks)

FastAPI, threading, and full Docker arrive here, because there is now something to serve.

Inference mechanics (KV cache, paged attention, continuous batching, speculative decoding):
- [Engineering behind LLM Inference](https://www.youtube.com/playlist?app=desktop&list=PLqO45Dg1pMhlDBZTMqVL2GU-14xYip2y2)
- [LLM inference questions](https://drive.google.com/file/d/1mfTzOnwn8yx4eKObjPvpd-B_toGkQ_tu/view)

Books, in this order:
- [AI Engineering Book] (Huyen) - closer to what you are doing
- [Designing Machine Learning Systems] (Huyen)

Ops:
- [LLMOps Questions](https://aman.ai/primers/ai/LLMOps/)
- [LLMOps playlist](https://www.youtube.com/playlist?list=PLQxDHpeGU14CG-wDgZDqFdjsWhWqtDGdi)

Serving stack and system design (doubles as interview prep):
- [FastAPI for AI Engineers]
- [Threading](https://realpython.com/intro-to-python-threading/)
- [Docker guide](https://freedium-mirror.cfd/https://medium.com/devlink-tips/the-only-docker-guide-youll-ever-need-beginner-to-expert-35eeedeac4e8) - full pass
- [Backend from first principles](https://www.youtube.com/playlist?list=PLui3EUkuMTPgZcV0QhQrOcwMPcBCcd_Q1)
- [Primer on sys-design](https://medium.com/@shivambhadani_/system-design-for-beginners-everything-you-need-in-one-article-c74eb702540b)
- [LLD System Design](https://interviewready.io/account)
- [The Accidental CTO](https://github.com/subhashchy/The-Accidental-CTO) - skim, context not curriculum

---

## Phase 5: RAG and agents (3-4 weeks, ship two things)

Last and short. Three weeks of work once you understand LLMs. Six months of confusion if attempted first.

RAG:
- [RAG Stanford lecture](https://www.youtube.com/watch?v=h-7S6HNq0Vg&list=PLJf-Umv9fV2O3RyomJhiri_dRcrtgifvC&index=28)
- [Emerging patterns in GenAI](https://martinfowler.com/articles/gen-ai-patterns/#PuttingTogetherARealisticRag)
- [Prod RAG](https://arpitbhayani.me/blogs/rag-production)
- [RAG Microsoft design and eval guide](https://learn.microsoft.com/en-us/azure/architecture/ai-ml/guide/rag/rag-solution-design-and-evaluation-guide)
- [RAG CampusX course](https://learnwith.campusx.in/s/courses/69d8037290a183fe36833265/take) 
- [LLM Evals](https://www.youtube.com/playlist?list=PLEneLIDJFpcA) - the part that separates shipping from demoing. Weight accordingly

Frameworks, one week hard timebox:
- [LangChain/LangGraph cheatsheet](https://sumanmichael.github.io/langgraph-cheatsheet/) + one build
- [LangGraph playlist](https://www.youtube.com/playlist?list=PLKnIA16_RmvYsvB8qkUQuJmJNuiCUJFPL) / [LangChain playlist](https://www.youtube.com/playlist?list=PLKnIA16_RmvaTbihpo4MtzVm4XOQa0ER0) - reference only

Agents, build before reading about frameworks:
- [How to build an agent](https://ghuntley.com/agent/) - 300 lines, the whole idea. Build it
- [How agents work under the hood](https://www.youtube.com/watch?v=87T8xE-_yeo)
- [Building effective agents (Anthropic)](https://www.anthropic.com/engineering/building-effective-agents)
- [Multi-agent research system (Anthropic)](https://www.anthropic.com/engineering/multi-agent-research-system)
- [Tau source](https://github.com/huggingface/tau) + [architecture doc](https://twotimespi.dev/internals/architecture/)
- [Practical guide to building agents (OpenAI)](https://cdn.openai.com/business-guides-and-resources/a-practical-guide-to-building-agents.pdf)
- [Agentic AI Interview](https://learn.manifoldailearning.com/services/agentic-interview)

**Gate:** a RAG + agent system you use daily. If you do not use it, it did not work.

---

## Parallel tracks (never phases)

- **Neetcode150** - [2/day from Phase 0 onward](https://neetcode.io/practice/practice/neetcode150). A warmup, not a block of study time. Plus ByteByteGo interview patterns
- **Vision/multimodal** - weekend track during Phases 2-4: [ViT](https://arxiv.org/abs/2010.11929), [CLIP](https://arxiv.org/abs/2103.00020), [VAE](https://arxiv.org/abs/1312.6114), [DDPM](https://arxiv.org/abs/2006.11239), [SAM](https://arxiv.org/abs/2304.02643), [Whisper](https://arxiv.org/abs/2212.04356). Put the [CNN recap](https://www.youtube.com/playlist?list=PLVZqlMpoM6kaJX_2lLKjEhWI0NlqHfqzp) immediately before ViT, also read and implement UNet
- **Writing** - one blog per phase, on the thing you just built. This is the leverage
- **Revision** - [The Hitchhiker's Guide to Agentic AI](https://arxiv.org/abs/2606.24937) (Roitman, June 2026). Single-author synthesis spanning Phases 2-5. Not for learning. Two uses: (a) after each phase, read only the matching chapter as a self-test - if you cannot spot what it flattens, you did not learn the phase; (b) whole thing in two sittings before interviews, for the taxonomies (agent design patterns, memory split, multi-agent topologies). Start with the [12-page visual summary](https://gist.github.com/vukrosic/9fb5a16da25101382f42b43939b74de5); if it surfaces nothing new, skip the book. Caveat: 51 points and 4 comments on HN, one comment on alphaXiv. No peer scrutiny. Do not repeat any number it states without tracing the primary source
- **Interview layer** - two weeks before actually interviewing, not now: [ML Interview Topics](https://silviasapora.github.io/blog/ml-interviews.html), [your interview page](https://samitmohan.in/interviews) (resume line by line, every project and blog), [How to land a frontier job](https://vladfeinberg.com/2026/05/10/how-to-land-a-job-at-a-frontier-lab.html) and use TensorTonic


---

## Projects + Blog

The original plan lists resources with no build targets. Four checkpoints, one per major phase:

1. GPT-2 from a blank file, under an hour, no reference (Phase 1)
2. A Triton attention kernel beating naive attention, with measured wall-clock and achieved bandwidth (Phase 2)
3. A fine-tuned model on a chosen task, with eval harness and a writeup of failures (Phase 3)
4. A RAG + agent system in daily use (Phase 5)

Rewrite all blogs from scratch.

---

## Timeline

Phases sum to roughly 6-9 months of contiguous effort
Track hours and completion through Phase 0, then recalibrate.
