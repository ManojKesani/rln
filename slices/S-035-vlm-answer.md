# S-035 VLM answering with image citations
Milestone: M7 Multimodal
Status: todo   <!-- todo | doing | done -->
Depends on: S-034

## Goal
Answers cite images and you can view them.

## Done when (runnable in 2 minutes)
1. The prompt includes retrieved images plus captions.
2. The answer cites image sources.
3. Visual hallucination spot-checked by hand.

## Backend tasks
- [ ] VLM prompt builder with images and captions.
- [ ] Image citations in the claim schema.

## Frontend tasks
- [ ] Image sources in the citation panel.

## Files to create or change
Imports and exports are design intent. Adjust when you build, and verify library names in current docs.

### Backend
| File | Does | Imports | Exports |
|---|---|---|---|
| `apps/api/app/multimodal/vlm.py` | Builds a prompt with images and captions | llm.factory | build_multimodal_prompt(question, chunks) |
| `apps/api/app/retrieval/citations.py (edit)` | Allow image claims | pydantic | ImageClaim |
| `apps/api/app/services/answering.py (edit)` | Use the VLM prompt when images are retrieved | multimodal.vlm | answer_with_citations |

### Frontend
| File | Does | Imports | Exports |
|---|---|---|---|
| `apps/web/src/components/ImageSource.tsx` | Image source card | (props) | ImageSource |
| `apps/web/src/components/SourcesPanel.tsx (edit)` | Include image sources | ImageSource | SourcesPanel |

## Contract
```
Write this before building (endpoint, request, response example, errors).
```

## Out of scope
Fine-tuning.

## Log (fill in as you go)
- Built:
- Deviations from the contract:
- How to test:
- Known gaps:
