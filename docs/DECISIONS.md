# DECISIONS (append-only; supersede instead of editing)

## D-001 Postgres + pgvector for app data and vectors
Why: one database, simpler Docker. Rejected: SQLite plus a separate vector store. Revisit if vector search becomes a bottleneck.

## D-002 LangChain is the core, not a custom provider layer
Why: the goal is LangChain/LangGraph fluency. Own code only for the model catalog, rate-limit capture and usage logging.

## D-003 Full Docker Compose from day one
Why: avoids rework later. Cost: slower first setup.

## D-004 Milestone 1 is chat with history and model selection
Why: the smallest slice that exercises UI, API, DB, LLM and trace. RAG later is chat plus retrieval.

## D-005 Redis + Arq for background jobs (PROPOSED, not confirmed)
Why: async-native and lighter than Celery. Affects S-001 (redis and worker services) and S-016. Revisit if the service count hurts.

## D-006 Local embeddings; collections record model and dimension
Why: free and CPU-friendly; changing the model must create a new collection.

## D-007 Public benchmarks with labels over hand-built data
Why: ground truth is built in. A few own documents stay for "does it feel right" checks.

## D-008 Work in milestones and slices, one at a time
Why: small, checkable steps. The slice file is the plan and the log: tasks, files, contract, done-when, notes.

## D-009 The UI is a data-flow viewer
Why: seeing data move through the pipeline teaches it. Visual spec: the Trillian mockup (https://claude.ai/artifact/3izZ2eZ9iUTXYP4Ju4MNjx).

## D-010 Security hardening and fine-tuning deferred
Why: scope, and a CPU-only machine.

## D-011 Project name is Trillian
Why: one word, easy in paths and Docker names. Parked ideas: Marvin for the verifier agent, Babelfish for the provider layer.

## D-012 The worker lives in apps/api/app/worker.py
Why: same code and image as the API with a different start command; a separate project would duplicate dependencies.
