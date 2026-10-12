# S-031 Graph viewer
Milestone: M6 LangGraph multi-agent
Status: todo   <!-- todo | doing | done -->
Depends on: S-030

## Goal
See the graph diagram and the state at each step.

## Done when (runnable in 2 minutes)
1. Read-only diagram of the graph.
2. Clicking a node shows its input and output state for a run.

## Backend tasks
- [ ] Endpoint returning graph structure and run states.

## Frontend tasks
- [ ] Agent graphs page (mockup).

## Files to create or change
Imports and exports are design intent. Adjust when you build, and verify library names in current docs.

### Backend
| File | Does | Imports | Exports |
|---|---|---|---|
| `apps/api/app/services/graphs.py (edit)` | Return graph structure and stored run states | langgraph | get_structure, get_run |
| `apps/api/app/routers/graphs.py (edit)` | GET /api/graphs/{name}/structure, GET /api/graph-runs/{id} | services.graphs | router |

### Frontend
| File | Does | Imports | Exports |
|---|---|---|---|
| `apps/web/src/components/GraphDiagram.tsx` | SVG nodes and edges | (props) | GraphDiagram |
| `apps/web/src/components/RunTrace.tsx` | Per-node input/output state | (props) | RunTrace |
| `apps/web/src/pages/GraphsPage.tsx (edit)` | Diagram plus trace | GraphDiagram, RunTrace | GraphsPage |

## Contract
```
Write this before building (endpoint, request, response example, errors).
```

## Out of scope
Editing the graph.

## Log (fill in as you go)
- Built:
- Deviations from the contract:
- How to test:
- Known gaps:
