# Study Plan

---

## Phase 1: Build the transformer until it's boring 

- [CS336 Spring 2025](https://cs336.stanford.edu/spring2025/) with assignments.
    - Once done, deep dive into each topic and implement, use claude to study
- [Life of a Token](https://www.aleksagordic.com/blog/transformer) 
- [Notes on essential LLM](https://alisawuffles.notion.site/alisa-s-book-of-llms)
- Karpathy Zero to Hero and build nanoGPT and "Let's reproduce GPT-2" and nanoChat
- [Looped Transformer](https://magazine.sebastianraschka.com/p/gpt-6-astra-looped-transformers-and)

Blog: Finish CS336 with notes/assignments. Looped Transformer and why it's special.

---

## Phase 2: Optimisation

- [Memory (drepper, cpumemory)](https://akkadia.org/drepper/cpumemory.pdf)
- [Thinking in JAX](https://docs.jax.dev/en/latest/notebooks/thinking_in_jax.html) 
- [How to Scale Your Model](https://jax-ml.github.io/scaling-book/) - exercises by hand.
- Alredge, [CUDA for Deep Learning](https://www.manning.com/books/cuda-for-deep-learning)
- [FlashAttention](https://arxiv.org/abs/2205.14135) 
- [FlashAttention 1-4](https://arxiv.org/pdf/2603.05451)
- [ThunderKittens](https://arxiv.org/pdf/2410.20399)
- [GPipe](https://arxiv.org/abs/1811.06965) 
- [Scaling Laws for Neural Language Models](https://arxiv.org/abs/2001.08361)
- [Chinchilla](https://arxiv.org/abs/2203.15556)
- [InstructGPT](https://arxiv.org/abs/2203.02155)
- [DPO](https://arxiv.org/abs/2305.18290)
- [Constitutional AI](https://arxiv.org/abs/2212.08073)
- [Build DeepSeek](https://www.youtube.com/playlist?list=PLPTV0NXA_ZSiOpKKlHCyOq9lnp-dLvlms) + [DeepSeek-V2](https://arxiv.org/abs/2405.04434) - MLA and MoE, back-fills the MoE lecture

Blog: Build a triton attention kernel, understanding optimisation in LLMs

---

## Phase 3: Fine-tuning

- [Fine Tuning LLMs](https://magazine.sebastianraschka.com/p/finetuning-large-language-models)
- [Fine tuning on a single GPU](https://sebastianraschka.com/blog/2023/llm-grad-accumulation.html)
- [PEFT and adapters](https://sebastianraschka.com/blog/2023/llm-finetuning-llama-adapter.html)
- [LoRA](https://sebastianraschka.com/blog/2023/llm-finetuning-lora.html)
- [Fine tuning pretrained transformers](https://magazine.sebastianraschka.com/p/using-and-finetuning-pretrained-transformers)

Papers: [LoRA](https://arxiv.org/abs/2106.09685), [QLoRA](https://arxiv.org/abs/2305.14314).
- Unsloth + HuggingFace docs.

Project and Blog: Case study to imitate: [qed-nano](https://huggingface.co/spaces/lm-provers/qed-nano-blogpost), Finish LLM Fine Tuning Interview Handbook

---

## Phase 4: Inference

Inference mechanics: KV cache, paged attention, continuous batching, speculative decoding.
- [How GPT is trained and served](https://www.youtube.com/watch?v=xmkSf5IS-zw&list=PLJf-Umv9fV2O3RyomJhiri_dRcrtgifvC&index=34)
- [100 days of inference](https://github.com/elizabetht/100-days-of-inference)
- [Engineering behind LLM Inference](https://www.youtube.com/playlist?app=desktop&list=PLqO45Dg1pMhlDBZTMqVL2GU-14xYip2y2)
- [LLM inference questions](https://drive.google.com/file/d/1mfTzOnwn8yx4eKObjPvpd-B_toGkQ_tu/view)
- [Chip Designing from Bottom Up](https://www.youtube.com/watch?v=oIk3R-sMX5o&list=PLJf-Umv9fV2O3RyomJhiri_dRcrtgifvC&index=35)

Blog: How is GPT trained and served, everything I learnt about Inference Engineering

Chip Huyen, AI Engineering.

Ops:
- [LLMOps questions](https://aman.ai/primers/ai/LLMOps/)
- [LLMOps playlist](https://www.youtube.com/playlist?list=PLQxDHpeGU14CG-wDgZDqFdjsWhWqtDGdi)
- FastAPI for AI Engineers
- [Threading](https://realpython.com/intro-to-python-threading/)
- [Backend from first principles](https://www.youtube.com/playlist?list=PLui3EUkuMTPgZcV0QhQrOcwMPcBCcd_Q1)
- [Primer on system design](https://medium.com/@shivambhadani_/system-design-for-beginners-everything-you-need-in-one-article-c74eb702540b)
- [Distributed training in PyTorch](https://www.youtube.com/watch?v=XoGvCBRnwLs)
- [SQL Revision](https://www.youtube.com/watch?v=rf57kE3HJD0&list=PLJf-Umv9fV2O3RyomJhiri_dRcrtgifvC&index=31)
- Docker & Kubernetes master: [Docker guide](https://freedium-mirror.cfd/https://medium.com/devlink-tips/the-only-docker-guide-youll-ever-need-beginner-to-expert-35eeedeac4e8)

Blog: Understanding systems and LLMOps

---

## Phase 5: RAG and agents 

RAG:
- [Emerging patterns in GenAI](https://martinfowler.com/articles/gen-ai-patterns/#PuttingTogetherARealisticRag)
- [Prod RAG](https://arpitbhayani.me/blogs/rag-production)
- [RAG design and eval guide](https://learn.microsoft.com/en-us/azure/architecture/ai-ml/guide/rag/rag-solution-design-and-evaluation-guide)
- [RAG CampusX course](https://learnwith.campusx.in/s/courses/69d8037290a183fe36833265/take)
- [LLM Evals](https://www.youtube.com/playlist?list=PLEneLIDJFpcA) 

Blog: Lessons from building RAGs 

Frameworks, one week, hard timebox:
- [LangChain/LangGraph cheatsheet](https://sumanmichael.github.io/langgraph-cheatsheet/) 

Agents, build one before reading about frameworks:
- [Illustrated Guide to Agents by Jay Alammar]
- [How to build an agent](https://ghuntley.com/agent/) - 300 lines. Build it first
- [How agents work under the hood](https://www.youtube.com/watch?v=87T8xE-_yeo)
- [Building effective agents](https://www.anthropic.com/engineering/building-effective-agents)
- [Multi-agent research system](https://www.anthropic.com/engineering/multi-agent-research-system)
- [Tau source](https://github.com/huggingface/tau) plus [architecture doc](https://twotimespi.dev/internals/architecture/)
- [Practical guide to building agents](https://cdn.openai.com/business-guides-and-resources/a-practical-guide-to-building-agents.pdf)
- [Agentic AI Interview](https://learn.manifoldailearning.com/services/agentic-interview)

Blog: Agentic AI Frameworks and lessons

Projects: PI agent, minitorch, end-to-end RAG for company
---

## Computer Vision

[ViT](https://arxiv.org/abs/2010.11929),
[CLIP](https://arxiv.org/abs/2103.00020), [VAE](https://arxiv.org/abs/1312.6114),
[DDPM](https://arxiv.org/abs/2006.11239), [SAM](https://arxiv.org/abs/2304.02643),
[Whisper](https://arxiv.org/abs/2212.04356). Put the
[CNN recap](https://www.youtube.com/playlist?list=PLVZqlMpoM6kaJX_2lLKjEhWI0NlqHfqzp) right before ViT. Implement UNet. 
[Youtube Playlist](https://www.youtube.com/playlist?list=PLJf-Umv9fV2O3RyomJhiri_dRcrtgifvC)
[RL](https://walkinglabs.github.io/hands-on-modern-rl/en/chapter01_cartpole/principles)
VLM Book
[Speculative Decoding](https://neurips2026-speculative-decoding.vercel.app/)

Blog: Computer Vision 101

**Interviews** -
[ML Interview Topics](https://silviasapora.github.io/blog/ml-interviews.html),
[Interview Page](https://samitmohan.in/interviews) 
[How to land a frontier job](https://vladfeinberg.com/2026/05/10/how-to-land-a-job-at-a-frontier-lab.html),
Illya's 30 Paper List
TensorTonic
---
