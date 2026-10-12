# S-022 Retrieval stage pipeline
Milestone: M4 RAG
Status: todo   <!-- todo | doing | done -->
Depends on: S-021

## Goal
Build retrieval as ordered stages and see what each one changed.

## Done when (runnable in 2 minutes)
1. Dense, BM25, RRF and cross-encoder stages run in order.
2. Waterfall shows candidate counts and time per stage.
3. Rank history shows each chunk moving between stages.

## Backend tasks
- [ ] Stage contract: (queries, candidates) -> (queries, candidates).
- [ ] Stages: dense, bm25, rrf, rerank.
- [ ] Pipeline runner that keeps rank history.

## Frontend tasks
- [ ] Stage waterfall and rank table on the RAG page.

## Files to create or change
Imports and exports are design intent. Adjust when you build, and verify library names in current docs.

### Backend
| File | Does | Imports | Exports |
|---|---|---|---|
| `apps/api/app/retrieval/types.py (edit)` | Candidate gains per-stage rank/score history | dataclasses | Candidate, StageTrace |
| `apps/api/app/retrieval/stages/base.py` | Stage protocol: (queries, candidates) -> (queries, candidates) | typing.Protocol | Stage, StageResult |
| `apps/api/app/retrieval/stages/dense.py` | Vector search stage | retrieval.search | DenseStage |
| `apps/api/app/retrieval/stages/bm25.py` | Keyword stage (rank_bm25 or Postgres full text, decide) | (decide) | Bm25Stage |
| `apps/api/app/retrieval/stages/rrf.py` | Reciprocal rank fusion | (none) | RrfStage |
| `apps/api/app/retrieval/stages/rerank.py` | Cross-encoder rerank on CPU | sentence_transformers.CrossEncoder | RerankStage |
| `apps/api/app/retrieval/pipeline.py` | Runs stages in order, records timings and rank history | stages | run_pipeline(stages, query) |
| `apps/api/app/services/rag.py (edit)` | Use run_pipeline | retrieval.pipeline | ask |

### Frontend
| File | Does | Imports | Exports |
|---|---|---|---|
| `apps/web/src/components/Waterfall.tsx` | Candidates and time per stage | (props) | Waterfall |
| `apps/web/src/components/RankTable.tsx` | Rank per stage for each chunk | (props) | RankTable |
| `apps/web/src/pages/RagPage.tsx (edit)` | Add both components | Waterfall, RankTable | RagPage |

## Contract
```
Write this before building (endpoint, request, response example, errors).
```

## Out of scope
LLM stages (HyDE, rewrite); loops.

## Notes
Probably too big: split into stages and UI.

## Log (fill in as you go)
- Built:
- Deviations from the contract:
- How to test:
- Known gaps:
