# S-030 Router, retriever, answerer, verifier
Milestone: M6 LangGraph multi-agent
Status: todo   <!-- todo | doing | done -->
Depends on: S-029

## Goal
A multi-step graph answers multi-hop questions better than one agent.

## Done when (runnable in 2 minutes)
1. Runs on a HotpotQA subset.
2. The verifier loops back at most N times.
3. Eval numbers vs single-agent RAG recorded.

## Backend tasks
- [ ] Four nodes with a retry loop.
- [ ] Eval comparison script.

## Frontend tasks
- [ ] Show the verifier verdict in the answer view.

## Files to create or change
Imports and exports are design intent. Adjust when you build, and verify library names in current docs.

### Backend
| File | Does | Imports | Exports |
|---|---|---|---|
| `apps/api/app/graphs/nodes/router.py` | Classifies the question | llm.factory | router_node |
| `apps/api/app/graphs/nodes/retriever.py` | Retrieves with a profile | retrieval.registry | retriever_node |
| `apps/api/app/graphs/nodes/answerer.py` | Answers with citations | services.answering | answerer_node |
| `apps/api/app/graphs/nodes/verifier.py` | Checks the answer, can loop back | retrieval.citations | verifier_node |
| `apps/api/app/graphs/multihop.py` | Wires the four nodes with a capped retry loop | langgraph.graph, nodes | build_graph() |
| `scripts/eval_hotpot.py` | Compares graph vs single agent on HotpotQA | evals.runner | (script) |

### Frontend
| File | Does | Imports | Exports |
|---|---|---|---|
| `apps/web/src/components/RunPanel.tsx (edit)` | Show the verifier verdict | (props) | RunPanel |

## Contract
```
Write this before building (endpoint, request, response example, errors).
```

## Out of scope
More agents.

## Log (fill in as you go)
- Built:
- Deviations from the contract:
- How to test:
- Known gaps:
