# S-003 Phoenix tracing wired in
Milestone: M0 Foundation
Status: todo   <!-- todo | doing | done -->
Depends on: S-001

## Goal
Every API call shows up as a trace in Phoenix from day one.

## Done when (runnable in 2 minutes)
1. GET /api/debug/trace (dev only) returns a trace_id.
2. The trace appears in Phoenix within seconds.
3. The trace has the service name and an HTTP span.

## Backend tasks
- [ ] Add OpenTelemetry and OpenInference packages.
- [ ] tracing.py: register with the Phoenix endpoint and project name from .env.
- [ ] Debug route, disabled outside dev.

## Frontend tasks
- [ ] None in this slice.

## Files to create or change
Imports and exports are design intent. Adjust when you build, and verify library names in current docs.

### Backend
| File | Does | Imports | Exports |
|---|---|---|---|
| `apps/api/app/tracing.py` | Registers the tracer with Phoenix at startup | phoenix.otel.register (arize-phoenix-otel), app.config.settings | setup_tracing() |
| `apps/api/app/routers/debug.py` | GET /api/debug/trace: makes a span, returns trace_id | fastapi.APIRouter, opentelemetry.trace | router |
| `apps/api/app/main.py (edit)` | Call setup_tracing(); mount debug router only in dev | tracing, routers.debug, config | app |

### Frontend
None in this slice.

## Contract
```
GET /api/debug/trace -> 200 {"trace_id": "<hex>"}
```

## Out of scope
LangChain instrumentation (S-004), custom spans, dashboards.

## Notes
Verify package and function names in the Phoenix docs.

## Log (fill in as you go)
- Built: tracing.py registers a Phoenix tracer provider (project from .env, explicit service.name "trillian-api") and instruments FastAPI, excluding /api/health. Dev-only GET /api/debug/trace (behind require_user) creates a child span and returns the trace id.
- Deviations from the contract: added opentelemetry-instrumentation-fastapi (needed for the HTTP span); setup_tracing(app) takes the app as an argument; explicit resource=Resource.create({"service.name": "trillian-api"}) in register(); debug route requires login, so curl needs the cookie jar.
- How to test: log in with -c jar.txt, then curl -b jar.txt localhost:8080/api/debug/trace, then open localhost:6006, project "trillian", and find the trace (GET /api/debug/trace with child debug.trace).
- Known gaps: worker is not traced; LangChain instrumentation comes in S-004; Phoenix span panel doesn't show resource attributes, so service.name was verified by printing provider.resource.attributes.