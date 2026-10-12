# S-028 Break it and fix it
Milestone: M5 Evals
Status: todo   <!-- todo | doing | done -->
Depends on: S-027

## Goal
Break the pipeline on purpose and diagnose it from traces.

## Done when (runnable in 2 minutes)
1. Five scripted breakages: bad chunk size, wrong embedding model, no reranker, poisoned doc, empty collection.
2. For each: symptom, trace evidence, root cause, fix, metric change in docs/DEVLOG.md.

## Backend tasks
- [ ] Write the breakage scripts and run the evals.

## Frontend tasks
- [ ] None in this slice.

## Files to create or change
Imports and exports are design intent. Adjust when you build, and verify library names in current docs.

### Backend
| File | Does | Imports | Exports |
|---|---|---|---|
| `scripts/breakages/bad_chunk_size.py` | Re-ingests with a bad chunk size and runs the eval | ingestion, evals.runner | (script) |
| `scripts/breakages/wrong_embedding.py` | Queries with a different embedding model | ingestion.embedders | (script) |
| `scripts/breakages/no_reranker.py` | Runs the profile without the rerank stage | retrieval.registry | (script) |
| `scripts/breakages/poisoned_doc.py` | Adds a misleading document | ingestion.pipeline | (script) |
| `scripts/breakages/empty_collection.py` | Queries an empty collection | retrieval.search | (script) |
| `docs/breakage_log.md` | Template: symptom, trace evidence, cause, fix, metric change | (none) | (notes) |

### Frontend
None in this slice.

## Contract
```
Write this before building (endpoint, request, response example, errors).
```

## Out of scope
New features.

## Notes
A learning slice, not a feature slice.

## Log (fill in as you go)
- Built:
- Deviations from the contract:
- How to test:
- Known gaps:
