# S-015 Chunk viewer
Milestone: M3 Ingestion and chunk viewer
Status: todo   <!-- todo | doing | done -->
Depends on: S-014

## Goal
See a document with its chunks colored and listed.

## Done when (runnable in 2 minutes)
1. Document view highlights chunks and overlaps.
2. Clicking a chunk highlights its text and the reverse.
3. Switching collection version redraws boundaries.

## Backend tasks
- [ ] Endpoints for document text and chunks with offsets.

## Frontend tasks
- [ ] Chunks page (mockup).

## Files to create or change
Imports and exports are design intent. Adjust when you build, and verify library names in current docs.

### Backend
| File | Does | Imports | Exports |
|---|---|---|---|
| `apps/api/app/schemas/ingestion.py (edit)` | DocumentOut, ChunkOut with offsets | pydantic | DocumentOut, ChunkOut |
| `apps/api/app/routers/ingestion.py (edit)` | GET /api/collections/{id}/documents, /api/documents/{id}, /api/documents/{id}/chunks | db.models | router |

### Frontend
| File | Does | Imports | Exports |
|---|---|---|---|
| `apps/web/src/pages/ChunksPage.tsx` | Collection and document pickers plus viewer | DocumentView, ChunkList | ChunksPage |
| `apps/web/src/components/DocumentView.tsx` | Text colored by chunk, overlaps marked | (props: text, chunks) | DocumentView |
| `apps/web/src/components/ChunkList.tsx` | Chunk cards, click to select | (props) | ChunkList |

## Contract
```
Write this before building (endpoint, request, response example, errors).
```

## Out of scope
Embedding map.

## Notes
Needs offsets from S-014.

## Log (fill in as you go)
- Built:
- Deviations from the contract:
- How to test:
- Known gaps:
