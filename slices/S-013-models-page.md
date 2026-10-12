# S-013 Models page
Milestone: M2 Agents, tools, token control
Status: todo   <!-- todo | doing | done -->
Depends on: S-012

## Goal
See each model, what it supports, and how much rate limit is left.

## Done when (runnable in 2 minutes)
1. Models page shows tool/vision/structured-output flags.
2. Remaining requests and tokens shown from real response headers.
3. An unavailable model is marked, not hidden.

## Backend tasks
- [ ] Capability flags per model.
- [ ] Capture rate-limit headers into rate_limit_snapshots.
- [ ] Endpoint for the page.

## Frontend tasks
- [ ] Models page (mockup).

## Files to create or change
Imports and exports are design intent. Adjust when you build, and verify library names in current docs.

### Backend
| File | Does | Imports | Exports |
|---|---|---|---|
| `apps/api/alembic/versions/0007_rate_limits.py` | rate_limit_snapshots table | alembic | upgrade(), downgrade() |
| `apps/api/app/db/models/rate_limit_snapshot.py` | provider, model, remaining requests/tokens, reset | db.base | RateLimitSnapshot |
| `apps/api/app/llm/rate_limits.py` | Parse and store rate-limit headers | db.session | capture_rate_limits(provider, model, headers) |
| `apps/api/app/llm/capabilities.py` | Table of tool/vision/structured-output flags | (none) | capabilities_for(provider, model) |
| `apps/api/app/routers/models.py (edit)` | Include capabilities and latest limits | llm.capabilities, llm.rate_limits | router |

### Frontend
| File | Does | Imports | Exports |
|---|---|---|---|
| `apps/web/src/pages/ModelsPage.tsx` | Table of models | CapabilityTags, hooks.useModels | ModelsPage |
| `apps/web/src/components/CapabilityTags.tsx` | Tags for tools/vision/json | (props) | CapabilityTags |

## Contract
```
Write this before building (endpoint, request, response example, errors).
```

## Out of scope
Polling providers, cost dashboards.

## Notes
May move after M4.

## Log (fill in as you go)
- Built:
- Deviations from the contract:
- How to test:
- Known gaps:
