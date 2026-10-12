# S-027 Experiment compare
Milestone: M5 Evals
Status: todo   <!-- todo | doing | done -->
Depends on: S-026

## Goal
Change a setting and see the delta against the old run.

## Done when (runnable in 2 minutes)
1. Compare two runs: config, metrics, cost.
2. Change one stage and see the delta.
3. A run is reproducible from its saved config.

## Backend tasks
- [ ] Save run configs.
- [ ] Compare endpoint with deltas.

## Frontend tasks
- [ ] Compare table (mockup).

## Files to create or change
Imports and exports are design intent. Adjust when you build, and verify library names in current docs.

### Backend
| File | Does | Imports | Exports |
|---|---|---|---|
| `apps/api/app/services/evals.py (edit)` | compare_runs(a, b) with deltas | db.models.eval_run | compare_runs |
| `apps/api/app/routers/evals.py (edit)` | GET /api/evals/compare?a=&b= | services.evals | router |

### Frontend
| File | Does | Imports | Exports |
|---|---|---|---|
| `apps/web/src/components/CompareTable.tsx` | Two runs with delta column | (props) | CompareTable |
| `apps/web/src/pages/EvalsPage.tsx (edit)` | Select two runs to compare | CompareTable | EvalsPage |

## Contract
```
Write this before building (endpoint, request, response example, errors).
```

## Out of scope
Dashboards.

## Log (fill in as you go)
- Built:
- Deviations from the contract:
- How to test:
- Known gaps:
