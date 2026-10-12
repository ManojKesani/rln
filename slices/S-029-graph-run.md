# S-029 Graph in code, run from UI
Milestone: M6 LangGraph multi-agent
Status: todo   <!-- todo | doing | done -->
Depends on: S-028

## Goal
Run a LangGraph graph and see each node in the trace.

## Done when (runnable in 2 minutes)
1. The graph runs from an endpoint.
2. Per-node spans appear in Phoenix.
3. State after each node is viewable.

## Backend tasks
- [ ] Graph in code.
- [ ] Run endpoint.
- [ ] Per-node spans and state capture.

## Frontend tasks
- [ ] Run button and trace link (minimal).

## Files to create or change
Imports and exports are design intent. Adjust when you build, and verify library names in current docs.

### Backend
| File | Does | Imports | Exports |
|---|---|---|---|
| `apps/api/app/graphs/state.py` | Shared graph state | typing.TypedDict | GraphState |
| `apps/api/app/graphs/simple_rag.py` | A small LangGraph graph | langgraph.graph, graphs.state | build_graph() |
| `apps/api/app/services/graphs.py` | Run a graph and capture state per node | graphs.simple_rag | run_graph(name, input) |
| `apps/api/app/routers/graphs.py` | POST /api/graphs/{name}/run | services.graphs | router |

### Frontend
| File | Does | Imports | Exports |
|---|---|---|---|
| `apps/web/src/pages/GraphsPage.tsx` | Run button and trace link | RunPanel | GraphsPage |
| `apps/web/src/components/RunPanel.tsx` | Input, output, trace link | (props) | RunPanel |

## Contract
```
Write this before building (endpoint, request, response example, errors).
```

## Out of scope
Drag-and-drop editing.

## Log (fill in as you go)
- Built:
- Deviations from the contract:
- How to test:
- Known gaps:
