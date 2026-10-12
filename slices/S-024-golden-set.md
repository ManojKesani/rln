# S-024 Golden set import
Milestone: M5 Evals
Status: todo   <!-- todo | doing | done -->
Depends on: S-023

## Goal
Import labeled SciFact questions as a frozen, versioned dataset.

## Done when (runnable in 2 minutes)
1. Dataset lists questions with relevant doc ids.
2. Includes some unanswerable questions.
3. Dataset is frozen and versioned.

## Backend tasks
- [ ] eval_datasets and eval_questions tables.
- [ ] Import script reading data/raw.

## Frontend tasks
- [ ] Evals page: dataset list (read-only).

## Files to create or change
Imports and exports are design intent. Adjust when you build, and verify library names in current docs.

### Backend
| File | Does | Imports | Exports |
|---|---|---|---|
| `apps/api/alembic/versions/0014_eval_datasets.py` | eval_datasets, eval_questions | alembic | upgrade(), downgrade() |
| `apps/api/app/db/models/eval_dataset.py` | name, version, frozen | db.base | EvalDataset |
| `apps/api/app/db/models/eval_question.py` | question, relevant doc ids, answerable flag | db.base | EvalQuestion |
| `scripts/import_scifact.py` | Loads SciFact corpus, queries and labels from data/raw | json, db.session | (script) |
| `apps/api/app/services/evals.py` | List datasets and questions | db.session | list_datasets, get_questions |
| `apps/api/app/routers/evals.py` | GET /api/evals/datasets, /datasets/{id}/questions | services.evals | router |

### Frontend
| File | Does | Imports | Exports |
|---|---|---|---|
| `apps/web/src/pages/EvalsPage.tsx` | Dataset list (read-only) | DatasetList | EvalsPage |
| `apps/web/src/components/DatasetList.tsx` | Datasets with question counts | (props) | DatasetList |

## Contract
```
Write this before building (endpoint, request, response example, errors).
```

## Out of scope
LLM-generated questions.

## Log (fill in as you go)
- Built:
- Deviations from the contract:
- How to test:
- Known gaps:
