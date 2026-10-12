# S-016 Background ingestion jobs
Milestone: M3 Ingestion and chunk viewer
Status: todo   <!-- todo | doing | done -->
Depends on: S-014

## Goal
Ingestion runs in the background with visible progress.

## Done when (runnable in 2 minutes)
1. A large ingest does not block the API.
2. Progress bar updates and finishes.
3. A failed job shows an error and can be retried.

## Backend tasks
- [ ] Arq worker and job functions.
- [ ] jobs table and status endpoint.
- [ ] Retry.

## Frontend tasks
- [ ] Progress bars and job list on the Ingestion page.

## Files to create or change
Imports and exports are design intent. Adjust when you build, and verify library names in current docs.

### Backend
| File | Does | Imports | Exports |
|---|---|---|---|
| `apps/api/app/worker.py` | Arq WorkerSettings and ingest_job | arq, ingestion.pipeline, services.jobs | WorkerSettings, ingest_job |
| `apps/api/alembic/versions/0009_jobs.py` | jobs table | alembic | upgrade(), downgrade() |
| `apps/api/app/db/models/job.py` | id, kind, status, progress, error | db.base | Job |
| `apps/api/app/services/jobs.py` | Enqueue and read jobs | arq, redis, db.session | enqueue_ingest, job_status, retry_job |
| `apps/api/app/ingestion/pipeline.py (edit)` | Report progress to the job row | services.jobs | ingest_file |
| `apps/api/app/routers/ingestion.py (edit)` | Upload enqueues; GET /api/jobs/{id}; POST retry | services.jobs | router |

### Frontend
| File | Does | Imports | Exports |
|---|---|---|---|
| `apps/web/src/components/JobProgress.tsx` | Progress bar with error and retry | hooks.useJob (refetchInterval) | JobProgress |
| `apps/web/src/pages/IngestionPage.tsx (edit)` | Job list | JobProgress | IngestionPage |

## Contract
```
Write this before building (endpoint, request, response example, errors).
```

## Out of scope
Scheduling.

## Notes
Depends on decision D-005.

## Log (fill in as you go)
- Built:
- Deviations from the contract:
- How to test:
- Known gaps:
