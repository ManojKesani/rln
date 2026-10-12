# S-019 vector_search tool on agents
Milestone: M4 RAG
Status: todo   <!-- todo | doing | done -->
Depends on: S-018, S-010

## Goal
An agent answers from a chosen collection.

## Done when (runnable in 2 minutes)
1. An agent with vector_search answers a SciFact question.
2. The tool records chunk ids and scores as an artifact.
3. An agent without the tool does not retrieve.

## Backend tasks
- [ ] vector_search tool taking a collection id.
- [ ] Attach it in the agent config.

## Frontend tasks
- [ ] Agents page: vector_search config with a collection dropdown.
- [ ] Collection dropdown in the chat header.

## Files to create or change
Imports and exports are design intent. Adjust when you build, and verify library names in current docs.

### Backend
| File | Does | Imports | Exports |
|---|---|---|---|
| `apps/api/app/retrieval/types.py` | Shared types | dataclasses | Candidate |
| `apps/api/app/retrieval/search.py` | Dense search over a collection | db.session, ingestion.embedders | dense_search(collection_id, query, k) |
| `apps/api/app/agents/tools/vector_search.py` | Tool factory bound to a collection; stores results as an artifact | langchain_core.tools, retrieval.search, services.artifacts | make_vector_search_tool(collection_id) |
| `apps/api/app/agents/builder.py (edit)` | Add the tool when the agent has it | vector_search | build_agent_from_row |
| `apps/api/app/db/models/agent.py (edit)` | collection_id | sqlalchemy | Agent |

### Frontend
| File | Does | Imports | Exports |
|---|---|---|---|
| `apps/web/src/components/AgentEditor.tsx (edit)` | Collection dropdown under vector_search | hooks.useCollections | AgentEditor |
| `apps/web/src/pages/ChatPage.tsx (edit)` | Collection dropdown in the header | hooks.useCollections | ChatPage |

## Contract
```
Write this before building (endpoint, request, response example, errors).
```

## Out of scope
Citations, advanced retrieval.

## Log (fill in as you go)
- Built:
- Deviations from the contract:
- How to test:
- Known gaps:
