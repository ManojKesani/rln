# S-026 LLM judge for faithfulness
Milestone: M5 Evals
Status: todo   <!-- todo | doing | done -->
Depends on: S-025

## Goal
Score answers for faithfulness without paying twice.

## Done when (runnable in 2 minutes)
1. The judge scores answers with structured output.
2. A second run costs zero tokens (cache).
3. Judge verdicts spot-checked against 10 of your labels.

## Backend tasks
- [ ] Judge prompt (versioned) and structured output.
- [ ] Cache.
- [ ] Spot-check script.

## Frontend tasks
- [ ] Faithfulness column in the results table.

## Files to create or change
Imports and exports are design intent. Adjust when you build, and verify library names in current docs.

### Backend
| File | Does | Imports | Exports |
|---|---|---|---|
| `apps/api/app/evals/judge.py` | Faithfulness judge with structured output, cached | llm.factory, pydantic | judge_faithfulness(answer, contexts) |
| `apps/api/app/evals/runner.py (edit)` | Optionally judge answers | evals.judge | run_retrieval_eval |
| `scripts/judge_spotcheck.py` | Compares the judge with your 10 labels | evals.judge | (script) |

### Frontend
| File | Does | Imports | Exports |
|---|---|---|---|
| `apps/web/src/components/ResultsTable.tsx (edit)` | Faithfulness column | (props) | ResultsTable |
| `apps/web/src/components/JudgeDetail.tsx` | Verdict and reason per answer | (props) | JudgeDetail |

## Contract
```
Write this before building (endpoint, request, response example, errors).
```

## Out of scope
Fine-tuned judges.

## Notes
Use a cheap model; note its reliability.

## Log (fill in as you go)
- Built:
- Deviations from the contract:
- How to test:
- Known gaps:
