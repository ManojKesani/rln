# S-033 Text-to-image retrieval
Milestone: M7 Multimodal
Status: todo   <!-- todo | doing | done -->
Depends on: S-032

## Goal
Search images with text and measure recall@k against captions.

## Done when (runnable in 2 minutes)
1. A text query returns relevant images.
2. Recall@k measured on captions.

## Backend tasks
- [ ] Text-to-image query endpoint.
- [ ] Recall@k script.

## Frontend tasks
- [ ] Image results in the RAG page.

## Files to create or change
Imports and exports are design intent. Adjust when you build, and verify library names in current docs.

### Backend
| File | Does | Imports | Exports |
|---|---|---|---|
| `apps/api/app/retrieval/stages/image_dense.py` | Text-to-image search stage | multimodal.clip | ImageDenseStage |
| `apps/api/app/routers/retrieval.py (edit)` | POST /api/rag/search-images | services.rag | router |
| `apps/api/app/evals/image_recall.py` | recall@k against captions | evals.metrics | image_recall_at_k |

### Frontend
| File | Does | Imports | Exports |
|---|---|---|---|
| `apps/web/src/components/ImageResults.tsx` | Grid of results with scores | (props) | ImageResults |
| `apps/web/src/pages/RagPage.tsx (edit)` | Image search tab | ImageResults | RagPage |

## Contract
```
Write this before building (endpoint, request, response example, errors).
```

## Out of scope
Image-to-text, video.

## Log (fill in as you go)
- Built:
- Deviations from the contract:
- How to test:
- Known gaps:
