# S-034 PDF figures and page retrieval
Milestone: M7 Multimodal
Status: todo   <!-- todo | doing | done -->
Depends on: S-033

## Goal
A question answerable only from a figure retrieves the right page.

## Done when (runnable in 2 minutes)
1. PDF text, tables and figures extracted.
2. Figures captioned and embedded.
3. A DocVQA/ViDoRe slice question retrieves the right page.

## Backend tasks
- [ ] PDF extraction pipeline.
- [ ] Figure captioning and embedding.
- [ ] Page retrieval.

## Frontend tasks
- [ ] Page and figure viewer in the sources panel.

## Files to create or change
Imports and exports are design intent. Adjust when you build, and verify library names in current docs.

### Backend
| File | Does | Imports | Exports |
|---|---|---|---|
| `apps/api/app/multimodal/pdf_figures.py` | Extract text, tables, figures, page images | pymupdf (decide) | extract_pdf(path) |
| `apps/api/app/multimodal/captions.py` | Caption a figure | llm.factory or local model | caption_image |
| `apps/api/app/ingestion/pipeline.py (edit)` | PDF path: text chunks + figure chunks | multimodal | ingest_file |
| `scripts/eval_docvqa.py` | Page retrieval check on a DocVQA/ViDoRe slice | evals.runner | (script) |

### Frontend
| File | Does | Imports | Exports |
|---|---|---|---|
| `apps/web/src/components/PageViewer.tsx` | Shows a page image | (props) | PageViewer |
| `apps/web/src/components/FigureCard.tsx` | Figure, caption, score | (props) | FigureCard |

## Contract
```
Write this before building (endpoint, request, response example, errors).
```

## Out of scope
Audio, video.

## Notes
Page-image retrieval is heavy on CPU: keep to a few hundred pages.

## Log (fill in as you go)
- Built:
- Deviations from the contract:
- How to test:
- Known gaps:
