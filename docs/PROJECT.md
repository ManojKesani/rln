# PROJECT: Trillian
One word, no spaces: repo, compose project and database are all `trillian`.

## Goal
Learn by building an LLM workbench that ends in multimodal RAG. Learning first; daily use is a bonus.
Machine: CPU only. Token budget: tight. Development must be cheap.

## Ranked priorities
1. Build and debug a RAG system and justify every design choice (is it retrieval, chunking, prompt or model?)
2. LangChain / LangGraph fluency, learned by building
3. Explain why one config beats another, with evidence (light eval harness)
4. Multimodal Q&A (late experiment, not a polished product)

## How we work
- Milestones (M0-M7) are demo-able outcomes. Each is made of slices (1-3 sessions each). One slice at a time.
- A slice file (`slices/S-0xx-*.md`) holds: goal, done-when checks, backend and frontend tasks, a Files table
  (does / imports / exports), the API contract, and a log.
- Per slice: `git switch -c s-0xx-name` -> `bash scripts/make-skeleton.sh 0xx` (creates the new files from the Files table)
  -> backend first, then frontend -> run the done-when checks -> fill the Log -> set Status done -> update STATUS.md and DEVLOG.md
  -> merge and tag.
- Contract before code: agree the endpoint shape in the slice file first. Changing it later means updating the slice file.
- New AI chat: paste PROJECT.md, ARCHITECTURE.md, the current slice file, the files it marks `(edit)`, and frontend-rules.md
  when it has frontend work. Ask it to restate the task and list its assumptions before writing code.

## Cross-cutting rules
- Token budget first: big tool output is stored by reference; only summaries enter the context.
- Cheap by default: fake model and LLM cache for development; real models only when evaluating.
- Everything traced in Phoenix. If it is not visible there, it is not done.
- Provenance everywhere: every chunk and answer traces back to its source.
- Every collection records its embedding model and dimension. Changing the model means a new collection.
- The UI is a data-flow viewer: each backend step gets a plain matching view.

## Stack
Backend: FastAPI, async SQLAlchemy 2, Alembic. DB: Postgres + pgvector. Queue: Redis + Arq (proposed, D-005).
LLM: LangChain core; Groq / OpenRouter / NVIDIA NIM through ChatOpenAI with base_url; a fake chat model for dev.
Embeddings: local (bge-small, MiniLM). Tracing: Phoenix + OpenInference.
Frontend: Vite, React, TSX, Tailwind, shadcn/ui, TanStack Query, typed client generated from openapi.json.
Infra: Docker Compose (nginx, web, api, worker, postgres, redis, phoenix). Auth: single user, JWT in an httpOnly cookie.
Verify library and API names against current official docs before relying on them.

## Datasets (frozen in data/raw, never fetched during evals)
SciFact / NFCorpus (BEIR), HotpotQA or MultiHop-RAG subset, SQuAD 2.0 unanswerables / RGB,
DocVQA / ViDoRe slice, Flickr8k, self-made duplicate files and personal notes.

## Out of scope for now
Security hardening, fine-tuning (CPU only), drag-and-drop graph editor.
