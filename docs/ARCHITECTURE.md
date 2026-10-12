# ARCHITECTURE

## Services (Docker Compose)
nginx -> web (S-001 placeholder, then the Vite build) and /api -> api (FastAPI).
api uses postgres (pgvector), redis and phoenix. worker (Arq) runs ingestion jobs from the same image as api
(code lives in apps/api/app/worker.py; there is no separate apps/worker). nginx has `proxy_buffering off` on /api for SSE.

```
Browser -> nginx -> web
                 \-> api -> LangChain agent -> provider (Groq / OpenRouter / NIM / fake)
                       |-> postgres (app data, checkpointer, vectors)
                       |-> redis -> worker (ingestion jobs)
                       \-> phoenix (OpenTelemetry traces)
```

## Chat data flow
UI -> POST /api/conversations/{id}/stream -> agent loop (tools) -> SSE events (token, tool_start, tool_end, usage, done)
-> llm_calls row + Phoenix trace. History: Postgres checkpointer keyed by thread_id; our own `conversations` table points to it.

## Core chain (M3-M4)
Ingestion profile -> collection version --\
                                           >-- vector_search tool -> agent
Retrieval profile (ordered stages) -------/
Stage contract: (queries, candidates) -> (queries, candidates); candidates keep rank/score history per stage.

## Data model (grows per milestone)
M1: conversations, llm_calls
M2: artifacts, agents, prompts (versioned), rate_limit_snapshots
M3: collections (embedding_model, dim), documents, chunks (offsets, provenance), jobs, embedding_cache, ingestion_profiles
M4: answers (claims, retrieved/cited ids), retrieval_profiles (stages as JSON, versioned)
M5: eval_datasets, eval_questions, eval_runs, eval_results

## Layout and layering
```
apps/api/app/
  routers/    thin HTTP layer only: parse, call a service, return a schema
  schemas/    Pydantic request/response models (the API contract; becomes openapi.json)
  services/   business logic, no HTTP
  db/         session, base, checkpointer, models/
  llm/        provider table, model factory, catalog, usage callback, capabilities, rate limits
  agents/     agent builder, tools/
  ingestion/  loaders, chunkers, embedders, pipeline, hashing, cache, dedupe
  retrieval/  types, search, citations, pipeline, registry, stages/
  evals/      metrics, runner, judge
  graphs/     LangGraph graphs defined in code (nodes/)
  multimodal/ clip, pdf_figures, captions, vlm
apps/web/src/ api/ (generated client, hooks), lib/, pages/, components/
```
Dependency direction: routers -> services -> (llm, agents, ingestion, retrieval, evals, graphs, multimodal) -> db.
The file-by-file plan, with what each file does, imports and exports, lives in each slice file.
Other top-level folders: nginx/, web-placeholder/, scripts/, data/raw/ (gitignored), docs/, slices/.
