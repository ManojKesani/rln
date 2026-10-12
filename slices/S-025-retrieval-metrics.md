# S-025 Retrieval metrics run
Milestone: M5 Evals
Status: todo   <!-- todo | doing | done -->
Depends on: S-024

## Goal
Run a retrieval profile over a dataset and get recall@k, MRR and nDCG.

## Done when (runnable in 2 minutes)
1. A run produces the three metrics.
2. Rerunning gives identical numbers.
3. Results are stored per question.

## Backend tasks
- [ ] Runner for a profile over a dataset.
- [ ] Metrics written by you.
- [ ] eval_runs and eval_results tables.

## Frontend tasks
- [ ] Run button and results table.

## Files to create or change
Imports and exports are design intent. Adjust when you build, and verify library names in current docs.

### Backend
| File | Does | Imports | Exports |
|---|---|---|---|
| `apps/api/app/evals/metrics.py` | recall@k, MRR, nDCG, written by you | math | recall_at_k, mrr, ndcg_at_k |
| `apps/api/alembic/versions/0015_eval_runs.py` | eval_runs and eval_results | alembic | upgrade(), downgrade() |
| `apps/api/app/db/models/eval_run.py` | dataset, collection, profile, config JSON, metrics | db.base | EvalRun, EvalResult |
| `apps/api/app/evals/runner.py` | Runs a profile over a dataset, stores per-question results | retrieval.registry, evals.metrics | run_retrieval_eval(dataset_id, collection_id, profile_id) |
| `apps/api/app/routers/evals.py (edit)` | POST /api/evals/runs, GET /runs/{id} | evals.runner | router |

### Frontend
| File | Does | Imports | Exports |
|---|---|---|---|
| `apps/web/src/components/RunForm.tsx` | Pick dataset, collection, profile, run | hooks | RunForm |
| `apps/web/src/components/ResultsTable.tsx` | Metrics and per-question rows | (props) | ResultsTable |

## Contract
```
Write this before building (endpoint, request, response example, errors).
```

## Out of scope
Answer quality.

## Log (fill in as you go)
- Built:
- Deviations from the contract:
- How to test:
- Known gaps:
