# S-021 RAG playground (single config)
Milestone: M4 RAG
Status: todo   <!-- todo | doing | done -->
Depends on: S-019

## Goal
Ask a question and see retrieved chunks, scores, final prompt and answer.

## Done when (runnable in 2 minutes)
1. Retrieved chunks and scores shown.
2. The final prompt is visible.
3. The Phoenix trace link works.

## Backend tasks
- [ ] Playground endpoint returning chunks, scores, prompt, answer, trace id.

## Frontend tasks
- [ ] RAG page, single config (mockup).

## Files to create or change
Imports and exports are design intent. Adjust when you build, and verify library names in current docs.

### Backend
| File | Does | Imports | Exports |
|---|---|---|---|
| `apps/api/app/schemas/rag.py` | Models for ask request and result | pydantic | AskRequest, AskResult |
| `apps/api/app/services/rag.py` | Retrieve, build prompt, answer, return everything | retrieval.search, services.answering | ask(collection_id, question) |
| `apps/api/app/routers/retrieval.py` | POST /api/rag/ask | services.rag | router |

### Frontend
| File | Does | Imports | Exports |
|---|---|---|---|
| `apps/web/src/pages/RagPage.tsx` | Question box, chunks, prompt, answer, trace link | RetrievedChunks, PromptViewer | RagPage |
| `apps/web/src/components/RetrievedChunks.tsx` | Chunks with score bars | (props) | RetrievedChunks |
| `apps/web/src/components/PromptViewer.tsx` | Shows the final prompt | (props) | PromptViewer |

## Contract
```
Write this before building (endpoint, request, response example, errors).
```

## Out of scope
Compare mode, profiles.

## Log (fill in as you go)
- Built:
- Deviations from the contract:
- How to test:
- Known gaps:
