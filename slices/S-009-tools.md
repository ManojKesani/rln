# S-009 Tools with results stored by reference
Milestone: M2 Agents, tools, token control
Status: todo   <!-- todo | doing | done -->
Depends on: S-008

## Goal
Agents can call tools, and big tool output never floods the context.

## Done when (runnable in 2 minutes)
1. Calculator tool works in a chat.
2. Big-output tool returns an artifact id and a short summary to the model.
3. Fetching the artifact returns the full output.
4. Note the token count with vs without the artifact.

## Backend tasks
- [ ] agents/tools: calculator, big_output.
- [ ] artifacts table and endpoint.
- [ ] Content-and-artifact tool return form.
- [ ] Tool start/end events in the stream.

## Frontend tasks
- [ ] Collapsible tool-call row in the chat.
- [ ] Link that opens the full artifact on a plain page.

## Files to create or change
Imports and exports are design intent. Adjust when you build, and verify library names in current docs.

### Backend
| File | Does | Imports | Exports |
|---|---|---|---|
| `apps/api/app/agents/tools/calculator.py` | Safe math tool | langchain_core.tools.tool | calculator |
| `apps/api/app/agents/tools/big_output.py` | Demo tool returning content + artifact reference | langchain_core.tools.tool, services.artifacts | big_output |
| `apps/api/app/agents/tools/__init__.py` | Tool registry | the tool modules | ALL_TOOLS (name -> tool) |
| `apps/api/alembic/versions/0003_artifacts.py` | Creates artifacts table | alembic | upgrade(), downgrade() |
| `apps/api/app/db/models/artifact.py` | id, kind, content, created_at | db.base | Artifact |
| `apps/api/app/services/artifacts.py` | Save and fetch artifacts | db.session, models.artifact | save_artifact(content, kind), get_artifact(id) |
| `apps/api/app/routers/artifacts.py` | GET /api/artifacts/{id} | services.artifacts | router |
| `apps/api/app/services/streaming.py (edit)` | Emit tool_start and tool_end events | agents | stream_reply |

### Frontend
| File | Does | Imports | Exports |
|---|---|---|---|
| `apps/web/src/components/ToolCallRow.tsx` | Collapsible tool call with summary and artifact link | (props) | ToolCallRow |
| `apps/web/src/pages/ArtifactPage.tsx` | Plain view of one artifact | hooks.useArtifact | ArtifactPage |
| `apps/web/src/lib/sse.ts (edit)` | Handle tool events | (none) | streamChat |

## Contract
```
Write this before building (endpoint, request, response example, errors).
```

## Out of scope
Agent management UI, web/SQL tools.

## Log (fill in as you go)
- Built:
- Deviations from the contract:
- How to test:
- Known gaps:
