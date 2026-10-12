# S-010 Named agents
Milestone: M2 Agents, tools, token control
Status: todo   <!-- todo | doing | done -->
Depends on: S-009

## Goal
Create named agents with a prompt and tools; chats are grouped per agent.

## Done when (runnable in 2 minutes)
1. Create an agent with a name, prompt text and tools.
2. Chat shows agents; picking one lists its chats and a New chat button.
3. The agent only uses its enabled tools.

## Backend tasks
- [ ] agents and agent_tools tables and endpoints.
- [ ] Agent builder uses the agent prompt and tools.
- [ ] Conversations link to an agent.

## Frontend tasks
- [ ] Agents page: list and editor with tool checkboxes (mockup).
- [ ] Chat sidebar grouped by agent.

## Files to create or change
Imports and exports are design intent. Adjust when you build, and verify library names in current docs.

### Backend
| File | Does | Imports | Exports |
|---|---|---|---|
| `apps/api/alembic/versions/0004_agents.py` | agents table and conversations.agent_id | alembic | upgrade(), downgrade() |
| `apps/api/app/db/models/agent.py` | id, name, prompt_text, provider, model, tools (list of names) | db.base | Agent |
| `apps/api/app/schemas/agents.py` | Response and request models | pydantic | AgentIn, AgentOut |
| `apps/api/app/services/agents.py` | Agent CRUD | db.session, models.agent | create_agent, list_agents, get_agent, update_agent |
| `apps/api/app/routers/agents.py` | Agent endpoints and GET /api/tools | services.agents, agents.tools.ALL_TOOLS | router |
| `apps/api/app/agents/builder.py (edit)` | Build from an Agent row (its prompt and tools) | agents.tools | build_agent_from_row(agent, ...) |

### Frontend
| File | Does | Imports | Exports |
|---|---|---|---|
| `apps/web/src/pages/AgentsPage.tsx` | List and edit agents | AgentEditor, hooks.useAgents | AgentsPage |
| `apps/web/src/components/AgentEditor.tsx` | Form: name, prompt, model, tools | ToolPicker | AgentEditor |
| `apps/web/src/components/ToolPicker.tsx` | Tool checkboxes from /api/tools | hooks.useTools | ToolPicker |
| `apps/web/src/components/ConversationList.tsx (edit)` | Group chats by agent | hooks.useAgents | ConversationList |

## Contract
```
Write this before building (endpoint, request, response example, errors).
```

## Out of scope
Prompt versioning, retrieval attachment.

## Log (fill in as you go)
- Built:
- Deviations from the contract:
- How to test:
- Known gaps:
