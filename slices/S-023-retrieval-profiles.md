# S-023 Retrieval profiles and compare
Milestone: M4 RAG
Status: todo   <!-- todo | doing | done -->
Depends on: S-022

## Goal
Save a pipeline as a named, versioned profile and attach it to an agent.

## Done when (runnable in 2 minutes)
1. Save v1, edit to v2.
2. An agent is pinned to a profile version.
3. Compare two collection+profile pairs on one question.
4. An incompatible pairing is warned.

## Backend tasks
- [ ] retrieval_profiles table (stages as JSON, versioned).
- [ ] Attach to agent config; compatibility check.
- [ ] Compare endpoint.

## Frontend tasks
- [ ] Profiles page with stage builder.
- [ ] Side-by-side compare on the RAG page.
- [ ] Profile dropdowns in the agent config.

## Files to create or change
Imports and exports are design intent. Adjust when you build, and verify library names in current docs.

### Backend
| File | Does | Imports | Exports |
|---|---|---|---|
| `apps/api/alembic/versions/0013_retrieval_profiles.py` | retrieval_profiles table | alembic | upgrade(), downgrade() |
| `apps/api/app/db/models/retrieval_profile.py` | name, version, stages JSON | db.base | RetrievalProfile |
| `apps/api/app/retrieval/registry.py` | Maps stage names to classes, builds a pipeline from a profile | retrieval.stages | STAGE_REGISTRY, build_pipeline(profile) |
| `apps/api/app/services/retrieval_profiles.py` | Save versions, load, check compatibility with a collection | db.session | save_profile, get_profile, check_compat(profile, collection) |
| `apps/api/app/routers/retrieval.py (edit)` | Profile endpoints, compare endpoint | services.retrieval_profiles | router |
| `apps/api/app/db/models/agent.py (edit)` | retrieval_profile_id, pin version | sqlalchemy | Agent |

### Frontend
| File | Does | Imports | Exports |
|---|---|---|---|
| `apps/web/src/pages/ProfilesPage.tsx` | Profiles list and editor | StageBuilder | ProfilesPage |
| `apps/web/src/components/StageBuilder.tsx` | Ordered stage list with params, add and reorder | (props) | StageBuilder |
| `apps/web/src/pages/RagPage.tsx (edit)` | Compare two collection+profile pairs | RetrievedChunks | RagPage |
| `apps/web/src/components/AgentEditor.tsx (edit)` | Retrieval profile dropdown and version pin | hooks.useProfiles | AgentEditor |

## Contract
```
Write this before building (endpoint, request, response example, errors).
```

## Out of scope
Evals.

## Log (fill in as you go)
- Built:
- Deviations from the contract:
- How to test:
- Known gaps:
