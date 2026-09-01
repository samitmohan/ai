# Study Plan

---

## Phase 0: Pre-req

- Read tinygrad and try to recreate it: Project: MiniTorch. Make it the very best that you can. Keep adding to this as you go along.
- Illya's 30 Paper List
- Karpathy Zero to Hero and build nanoGPT and "Let's reproduce GPT-2" and nanoChat
- Docker & Kubernetes master: [Docker guide](https://freedium-mirror.cfd/https://medium.com/devlink-tips/the-only-docker-guide-youll-ever-need-beginner-to-expert-35eeedeac4e8)

---

## Phase 1: Build the transformer until it's boring 

- Raschka, Building LLMs from Scratch 
- [Life of a Token](https://www.aleksagordic.com/blog/transformer) 
- [Raschka LLM Architecture Gallery](https://sebastianraschka.com/llm-architecture-gallery/) 
- [Notes on essential LLM](https://alisawuffles.notion.site/alisa-s-book-of-llms)
- [CS336 Spring 2025](https://cs336.stanford.edu/spring2025/) with assignments.



---

## Phase 2: CS336, all five assignments 

- [Memory (drepper, cpumemory)](https://akkadia.org/drepper/cpumemory.pdf)
- Alredge, [CUDA for Deep Learning](https://www.manning.com/books/cuda-for-deep-learning)
- [FlashAttention](https://arxiv.org/abs/2205.14135) 
- [FlashAttention 1-4](https://arxiv.org/pdf/2603.05451)
- [ThunderKittens](https://arxiv.org/pdf/2410.20399)
- [GPipe](https://arxiv.org/abs/1811.06965) 
- [Thinking in JAX](https://docs.jax.dev/en/latest/notebooks/thinking_in_jax.html) 
- [How to Scale Your Model](https://jax-ml.github.io/scaling-book/) - exercises by hand.
- [Scaling Laws for Neural Language Models](https://arxiv.org/abs/2001.08361)
- [Chinchilla](https://arxiv.org/abs/2203.15556)
- [InstructGPT](https://arxiv.org/abs/2203.02155)
- [DPO](https://arxiv.org/abs/2305.18290)
- [Constitutional AI](https://arxiv.org/abs/2212.08073)
- [Build DeepSeek](https://www.youtube.com/playlist?list=PLPTV0NXA_ZSiOpKKlHCyOq9lnp-dLvlms) + [DeepSeek-V2](https://arxiv.org/abs/2405.04434) - MLA and MoE, back-fills the MoE lecture
- Building a reasoning model Raschka

Build a triton attention kernel and start working on Nutrify ?

---

## Phase 3: Fine-tuning

- [Fine Tuning LLMs](https://magazine.sebastianraschka.com/p/finetuning-large-language-models)
- [Fine tuning on a single GPU](https://sebastianraschka.com/blog/2023/llm-grad-accumulation.html)
- [PEFT and adapters](https://sebastianraschka.com/blog/2023/llm-finetuning-llama-adapter.html)
- [LoRA](https://sebastianraschka.com/blog/2023/llm-finetuning-lora.html)
- [Fine tuning pretrained transformers](https://magazine.sebastianraschka.com/p/using-and-finetuning-pretrained-transformers)

Papers: [LoRA](https://arxiv.org/abs/2106.09685), [QLoRA](https://arxiv.org/abs/2305.14314).
- Unsloth + HuggingFace docs.

Project: Case study to imitate: [qed-nano](https://huggingface.co/spaces/lm-provers/qed-nano-blogpost),
Revision: LLM Fine Tuning Interview Handbook

Project: Nutrify

---

## Phase 4: Inference

Inference mechanics: KV cache, paged attention, continuous batching, speculative decoding.
- [100 days of inference](https://github.com/elizabetht/100-days-of-inference)
- [Engineering behind LLM Inference](https://www.youtube.com/playlist?app=desktop&list=PLqO45Dg1pMhlDBZTMqVL2GU-14xYip2y2)
- [LLM inference questions](https://drive.google.com/file/d/1mfTzOnwn8yx4eKObjPvpd-B_toGkQ_tu/view)

Chip Huyen, AI Engineering.

Ops:
- [LLMOps questions](https://aman.ai/primers/ai/LLMOps/)
- [LLMOps playlist](https://www.youtube.com/playlist?list=PLQxDHpeGU14CG-wDgZDqFdjsWhWqtDGdi)

- FastAPI for AI Engineers
- [Threading](https://realpython.com/intro-to-python-threading/)
- [Backend from first principles](https://www.youtube.com/playlist?list=PLui3EUkuMTPgZcV0QhQrOcwMPcBCcd_Q1)
- [Primer on system design](https://medium.com/@shivambhadani_/system-design-for-beginners-everything-you-need-in-one-article-c74eb702540b)
- [LLD System Design](https://interviewready.io/account)
- [The Accidental CTO](https://github.com/subhashchy/The-Accidental-CTO) 
- [Distributed training in PyTorch](https://www.youtube.com/watch?v=XoGvCBRnwLs)

Project: Continue building minitorch

---

## Phase 5: RAG and agents 

RAG:
- [RAG Stanford lecture](https://www.youtube.com/watch?v=h-7S6HNq0Vg&list=PLJf-Umv9fV2O3RyomJhiri_dRcrtgifvC&index=28)
- [Emerging patterns in GenAI](https://martinfowler.com/articles/gen-ai-patterns/#PuttingTogetherARealisticRag)
- [Prod RAG](https://arpitbhayani.me/blogs/rag-production)
- [RAG design and eval guide](https://learn.microsoft.com/en-us/azure/architecture/ai-ml/guide/rag/rag-solution-design-and-evaluation-guide)
- [RAG CampusX course](https://learnwith.campusx.in/s/courses/69d8037290a183fe36833265/take)
- [LLM Evals](https://www.youtube.com/playlist?list=PLEneLIDJFpcA) 

Frameworks, one week, hard timebox:
- [LangChain/LangGraph cheatsheet](https://sumanmichael.github.io/langgraph-cheatsheet/) 

Agents, build one before reading about frameworks:
- [How to build an agent](https://ghuntley.com/agent/) - 300 lines. Build it first
- [How agents work under the hood](https://www.youtube.com/watch?v=87T8xE-_yeo)
- [Building effective agents](https://www.anthropic.com/engineering/building-effective-agents)
- [Multi-agent research system](https://www.anthropic.com/engineering/multi-agent-research-system)
- [Tau source](https://github.com/huggingface/tau) plus [architecture doc](https://twotimespi.dev/internals/architecture/)
- [Practical guide to building agents](https://cdn.openai.com/business-guides-and-resources/a-practical-guide-to-building-agents.pdf)
- [Agentic AI Interview](https://learn.manifoldailearning.com/services/agentic-interview)


Project: build an end-to-end RAG, PI agent, learn orchaestration

---

## More Resources

[ViT](https://arxiv.org/abs/2010.11929),
[CLIP](https://arxiv.org/abs/2103.00020), [VAE](https://arxiv.org/abs/1312.6114),
[DDPM](https://arxiv.org/abs/2006.11239), [SAM](https://arxiv.org/abs/2304.02643),
[Whisper](https://arxiv.org/abs/2212.04356). Put the
[CNN recap](https://www.youtube.com/playlist?list=PLVZqlMpoM6kaJX_2lLKjEhWI0NlqHfqzp) right before ViT. Implement UNet. 

**Revision** - [The Hitchhiker's Guide to Agentic AI](https://arxiv.org/abs/2606.24937)

**Interviews** -
[ML Interview Topics](https://silviasapora.github.io/blog/ml-interviews.html),
[Interview Page](https://samitmohan.in/interviews) 
[How to land a frontier job](https://vladfeinberg.com/2026/05/10/how-to-land-a-job-at-a-frontier-lab.html),
TensorTonic.

---

[Revision doc](https://docs.google.com/document/d/e/2PACX-1vQD8IlBotGdBxp3BnXkSjk8bNZlPV_0EH9ZA6wHd5dNf-BLSiwXUinvgv8ZoBEnNyTCF-chWO30NRw0/pub)

---
