# S-020 Citations with verification
Milestone: M4 RAG
Status: todo   <!-- todo | doing | done -->
Depends on: S-019

## Goal
See which passage supports each claim; unverifiable claims are flagged.

## Done when (runnable in 2 minutes)
1. Answers come back as claims with chunk ids and quotes.
2. A quote not found in its chunk is marked unverified.
3. Clicking [n] shows the passage highlighted.
4. An unanswerable question gives "not in sources".

## Backend tasks
- [ ] Claim schema and structured output.
- [ ] Quote verification (substring check).
- [ ] Store retrieved vs cited chunks.

## Frontend tasks
- [ ] Citation markers, sources panel, unverified state, retrieved-not-used list (mockup).

## Files to create or change
Imports and exports are design intent. Adjust when you build, and verify library names in current docs.

### Backend
| File | Does | Imports | Exports |
|---|---|---|---|
| `apps/api/app/retrieval/citations.py` | Claim schema and quote verification | pydantic | Claim, AnswerWithClaims, verify_claims(answer, chunks) |
| `apps/api/app/services/answering.py` | Answer with structured claims over retrieved chunks | llm.factory, retrieval.search, citations | answer_with_citations |
| `apps/api/alembic/versions/0012_answers.py` | answers table (claims, retrieved ids, cited ids) | alembic | upgrade(), downgrade() |
| `apps/api/app/db/models/answer.py` | Stores claims and retrieved/cited chunk ids | db.base | Answer |
| `apps/api/app/schemas/chat.py (edit)` | Add claims to message output | pydantic | MessageOut |

### Frontend
| File | Does | Imports | Exports |
|---|---|---|---|
| `apps/web/src/components/CitationText.tsx` | Text with clickable [n] markers | (props) | CitationText |
| `apps/web/src/components/SourcesPanel.tsx` | Used sources, retrieved-not-used | SourceCard | SourcesPanel |
| `apps/web/src/components/SourceCard.tsx` | Passage with the quote highlighted, verified flag | (props) | SourceCard |

## Contract
```
Write this before building (endpoint, request, response example, errors).
```

## Out of scope
Image citations, NLI scoring.

## Log (fill in as you go)
- Built:
- Deviations from the contract:
- How to test:
- Known gaps:
