# Study Plan

---

## Phase 0: Pre-req

- [Essential Math](https://alisawuffles.notion.site/math-notes#3737eb87360580b3b555e3c616713286) - only the rusty parts: linalg, probability, matrix calculus, napkin math
- Karpathy Zero to Hero - all 8 videos, typed by hand into a blank file
- Docker basics - 3 hours: build, run, `-v`, `--gpus all`. Full pass in Phase 4
- Papers, after nanoGPT runs:
  - [Understanding LSTM Networks](https://colah.github.io/posts/2015-08-Understanding-LSTMs/)
  - [Attention Is All You Need](https://arxiv.org/abs/1706.03762)
  - [AlexNet](https://papers.nips.cc/paper/2012/hash/c399862d3b9d6b76c8436e924a68c45b-Abstract.html) - skim
  - [Deep Residual Learning (ResNet)](https://arxiv.org/abs/1512.03385) - skim

**Gate:** nanoGPT trains, typed from an empty file.

---

## Phase 1: Build the transformer until it's boring (4-6 weeks)

- Raschka, Building LLMs from Scratch - second pass on purpose. Adds GPT-2 weight loading and task heads
- [Life of a Token](https://www.aleksagordic.com/blog/transformer) - tokenizer through sampling in one pass
- Karpathy, "Let's reproduce GPT-2 (124M)"
- Karpathy **nanochat** - pretrain, SFT, RL, chat UI in one repo. Run the whole pipeline once before CS336 has you build each piece
- Architecture deltas (RoPE, RMSNorm, GQA, SwiGLU):
  - [GPT-3](https://arxiv.org/abs/2005.14165)
  - [LLaMA 2](https://arxiv.org/abs/2307.09288)
  - [Mistral 7B](https://arxiv.org/abs/2310.06825)
  - [Raschka LLM Architecture Gallery](https://sebastianraschka.com/llm-architecture-gallery/) - side-by-side comparisons, use as reference
- [Notes on essential LLM](https://alisawuffles.notion.site/alisa-s-book-of-llms) - keep open
- minitorch Phases 1 through 3. Same layers, own autograd

**Gate:** [GPT-2 from an empty file, no reference, under an hour, and it trains](https://www.youtube.com/watch?v=xmkSf5IS-zw&t=1636s). Repeat until true. Do not start Phase 2 before passing.

---

## Phase 2: CS336, all five assignments (8-12 weeks)

[CS336 Spring 2025](https://cs336.stanford.edu/spring2025/)

### A1: Basics (tokenizer, architecture, optimizer, training)
No companion reading. Phase 1 was the prep. Lands in minitorch Phases 3 and 4.

### A2: Systems (profiling, Triton FlashAttention2, distributed training)
Read in this order:
- [Memory (drepper, cpumemory)](https://akkadia.org/drepper/cpumemory.pdf) - the memory hierarchy chapters
- Alredge, [CUDA for Deep Learning](https://www.manning.com/books/cuda-for-deep-learning) - read it here, with your own slow kernel to fix
- [FlashAttention](https://arxiv.org/abs/2205.14135) - v1, deep
- [FlashAttention 1-4](https://arxiv.org/pdf/2603.05451) - skim for the deltas
- [ThunderKittens](https://arxiv.org/pdf/2410.20399)
- [GPipe](https://arxiv.org/abs/1811.06965) - during the parallelism lectures

### A3: Scaling (scaling-law fitting)
- [Thinking in JAX](https://docs.jax.dev/en/latest/notebooks/thinking_in_jax.html) - one day
- [How to Scale Your Model](https://jax-ml.github.io/scaling-book/) - exercises by hand. Ch.1 roofline and Ch.4 transformer math are the pages that matter
- [Scaling Laws for Neural Language Models](https://arxiv.org/abs/2001.08361)
- [Chinchilla](https://arxiv.org/abs/2203.15556)

### A4: Data (CommonCrawl filtering, dedup)
No companion reading.

### A5: Alignment and reasoning RL (SFT + RL for math)
- [InstructGPT](https://arxiv.org/abs/2203.02155)
- [DPO](https://arxiv.org/abs/2305.18290)
- [Constitutional AI](https://arxiv.org/abs/2212.08073)
- [Build DeepSeek](https://www.youtube.com/playlist?list=PLPTV0NXA_ZSiOpKKlHCyOq9lnp-dLvlms) + [DeepSeek-V2](https://arxiv.org/abs/2405.04434) - MLA and MoE, back-fills the MoE lecture
- Building a reasoning model

**Gate:** a Triton attention kernel that beats the naive version, with measured wall-clock and achieved bandwidth.

---

## Phase 3: Fine-tuning (3-4 weeks)

- [Fine Tuning LLMs](https://magazine.sebastianraschka.com/p/finetuning-large-language-models)
- [Fine tuning on a single GPU](https://sebastianraschka.com/blog/2023/llm-grad-accumulation.html) - gradient accumulation
- [PEFT and adapters](https://sebastianraschka.com/blog/2023/llm-finetuning-llama-adapter.html)
- [LoRA](https://sebastianraschka.com/blog/2023/llm-finetuning-lora.html)
- [Fine tuning pretrained transformers](https://magazine.sebastianraschka.com/p/using-and-finetuning-pretrained-transformers)

Papers: [LoRA](https://arxiv.org/abs/2106.09685), [QLoRA](https://arxiv.org/abs/2305.14314).

Then Unsloth on bqa3.

Case study to imitate: [qed-nano](https://huggingface.co/spaces/lm-provers/qed-nano-blogpost),
teaching a tiny model to prove hard theorems.

LLM Fine Tuning Interview Handbook - a checklist for the end, not a textbook to read.

**Gate:** a fine-tuned model on a task you chose, with an eval harness and a writeup of what failed.

---

## Phase 4: Inference and serving (4-6 weeks)

FastAPI, threading, and the full Docker pass land here, because there is finally something to serve.

Inference mechanics: KV cache, paged attention, continuous batching, speculative decoding.
- [100 days of inference](https://github.com/elizabetht/100-days-of-inference)
- [Engineering behind LLM Inference](https://www.youtube.com/playlist?app=desktop&list=PLqO45Dg1pMhlDBZTMqVL2GU-14xYip2y2)
- [LLM inference questions](https://drive.google.com/file/d/1mfTzOnwn8yx4eKObjPvpd-B_toGkQ_tu/view)

Books, in this order: Huyen, AI Engineering. Then Huyen, Designing Machine Learning Systems.

Ops:
- [LLMOps questions](https://aman.ai/primers/ai/LLMOps/)
- [LLMOps playlist](https://www.youtube.com/playlist?list=PLQxDHpeGU14CG-wDgZDqFdjsWhWqtDGdi)

Serving and system design, which doubles as interview prep:
- FastAPI for AI Engineers
- [Threading](https://realpython.com/intro-to-python-threading/)
- [Docker guide](https://freedium-mirror.cfd/https://medium.com/devlink-tips/the-only-docker-guide-youll-ever-need-beginner-to-expert-35eeedeac4e8) - full pass
- [Backend from first principles](https://www.youtube.com/playlist?list=PLui3EUkuMTPgZcV0QhQrOcwMPcBCcd_Q1)
- [Primer on system design](https://medium.com/@shivambhadani_/system-design-for-beginners-everything-you-need-in-one-article-c74eb702540b)
- [LLD System Design](https://interviewready.io/account)
- [The Accidental CTO](https://github.com/subhashchy/The-Accidental-CTO) - skim for context
- [Distributed training in PyTorch](https://www.youtube.com/watch?v=XoGvCBRnwLs)

**Gate:** your Phase 3 fine-tune served behind an API, with measured p50 and p99
latency and tokens/sec under concurrent load.

---

## Phase 5: RAG and agents (3-4 weeks, ship two things)

RAG:
- [RAG Stanford lecture](https://www.youtube.com/watch?v=h-7S6HNq0Vg&list=PLJf-Umv9fV2O3RyomJhiri_dRcrtgifvC&index=28)
- [Emerging patterns in GenAI](https://martinfowler.com/articles/gen-ai-patterns/#PuttingTogetherARealisticRag)
- [Prod RAG](https://arpitbhayani.me/blogs/rag-production)
- [RAG design and eval guide](https://learn.microsoft.com/en-us/azure/architecture/ai-ml/guide/rag/rag-solution-design-and-evaluation-guide)
- [RAG CampusX course](https://learnwith.campusx.in/s/courses/69d8037290a183fe36833265/take)
- [LLM Evals](https://www.youtube.com/playlist?list=PLEneLIDJFpcA) - evals are how you know whether it works. Do not skip

Frameworks, one week, hard timebox:
- [LangChain/LangGraph cheatsheet](https://sumanmichael.github.io/langgraph-cheatsheet/) plus one build
- [LangGraph playlist](https://www.youtube.com/playlist?list=PLKnIA16_RmvYsvB8qkUQuJmJNuiCUJFPL) and [LangChain playlist](https://www.youtube.com/playlist?list=PLKnIA16_RmvaTbihpo4MtzVm4XOQa0ER0) - reference only

Agents, build one before reading about frameworks:
- [How to build an agent](https://ghuntley.com/agent/) - 300 lines. Build it first
- [How agents work under the hood](https://www.youtube.com/watch?v=87T8xE-_yeo)
- [Building effective agents](https://www.anthropic.com/engineering/building-effective-agents)
- [Multi-agent research system](https://www.anthropic.com/engineering/multi-agent-research-system)
- [Tau source](https://github.com/huggingface/tau) plus [architecture doc](https://twotimespi.dev/internals/architecture/)
- [Practical guide to building agents](https://cdn.openai.com/business-guides-and-resources/a-practical-guide-to-building-agents.pdf)
- [Agentic AI Interview](https://learn.manifoldailearning.com/services/agentic-interview)

**Gate:** a RAG and agent system you use daily for two weeks.

---

## Side tracks

**Neetcode150** - [2/day from Phase 0 onward](https://neetcode.io/practice/practice/neetcode150).

**Vision and multimodal** - weekends during Phases 2 to 4. [ViT](https://arxiv.org/abs/2010.11929),
[CLIP](https://arxiv.org/abs/2103.00020), [VAE](https://arxiv.org/abs/1312.6114),
[DDPM](https://arxiv.org/abs/2006.11239), [SAM](https://arxiv.org/abs/2304.02643),
[Whisper](https://arxiv.org/abs/2212.04356). Put the
[CNN recap](https://www.youtube.com/playlist?list=PLVZqlMpoM6kaJX_2lLKjEhWI0NlqHfqzp)
right before ViT. Implement UNet. Most of this lands in minitorch Phase 8.

**Revision** - [The Hitchhiker's Guide to Agentic AI](https://arxiv.org/abs/2606.24937)
(Roitman, June 2026). Use it as a self-test: after each phase read only the matching
chapter, and if you cannot spot what it flattens, you did not learn the phase. Start
with the [12-page visual summary](https://gist.github.com/vukrosic/9fb5a16da25101382f42b43939b74de5)
and skip the book if that surfaces nothing new. 51 points on HN, one comment on
alphaXiv, no peer scrutiny. Do not repeat a number from it without tracing the source.

**Interviews** - two weeks before interviewing, not now.
[ML Interview Topics](https://silviasapora.github.io/blog/ml-interviews.html),
[your interview page](https://samitmohan.in/interviews) rewritten resume line by line,
[How to land a frontier job](https://vladfeinberg.com/2026/05/10/how-to-land-a-job-at-a-frontier-lab.html),
and TensorTonic.

---

## Checkpoints

One per phase. Each is a build, not a reading.

1. GPT-2 from a blank file, under an hour, no reference (Phase 1)
2. A Triton attention kernel beating naive attention, with measured wall-clock and achieved bandwidth (Phase 2)
3. minitorch runs everything
4. A fine-tuned model on a chosen task, with eval harness and a writeup of failures (Phase 3)
5. Your fine-tune served behind an API with measured latency (Phase 4)
6. A RAG and agent system in daily use (Phase 5)

Rewrite the blogs from scratch as each checkpoint lands.

---

## Timeline

6-9 months.

[Revision doc](https://docs.google.com/document/d/e/2PACX-1vQD8IlBotGdBxp3BnXkSjk8bNZlPV_0EH9ZA6wHd5dNf-BLSiwXUinvgv8ZoBEnNyTCF-chWO30NRw0/pub)

---