# S-006 SSE streaming with usage event
Milestone: M1 Chat with history and model selection
Status: todo   <!-- todo | doing | done -->
Depends on: S-005

## Goal
See the reply token by token.

## Done when (runnable in 2 minutes)
1. curl -N shows token events as they arrive.
2. The last events are usage and done.
3. A mid-stream error produces an error event, not a hang.
4. Works through nginx.

## Backend tasks
- [ ] Streaming endpoint using one of the stream modes (try each and pick).
- [ ] Events: token, usage, done, error.
- [ ] Confirm nginx buffering is off.

## Frontend tasks
- [ ] None in this slice.

## Files to create or change
Imports and exports are design intent. Adjust when you build, and verify library names in current docs.

### Backend
| File | Does | Imports | Exports |
|---|---|---|---|
| `apps/api/app/schemas/chat.py (edit)` | Add SSE event payload models | pydantic | TokenEvent, UsageEvent, ErrorEvent |
| `apps/api/app/services/streaming.py` | Streams an agent run and formats it as SSE | services.chat, agents.builder, schemas.chat | sse(event, data), stream_reply(conversation_id, content) |
| `apps/api/app/routers/conversations.py (edit)` | POST /{id}/stream returning text/event-stream | fastapi.responses.StreamingResponse, services.streaming | router |

### Frontend
None in this slice.

## Contract
```
POST /api/conversations/{id}/stream {"content"} -> text/event-stream
event: token data: {"delta"}
event: usage data: {"input", "output", "latency_ms"}
event: done data: {}
event: error data: {"message"}
```

## Out of scope
Tool events, cancel button.

## Log (fill in as you go)
- Built: POST /api/conversations/{id}/stream (text/event-stream) using agent.astream(stream_mode="messages"); events token, usage (input, output, latency_ms), done, error. Usage is read from the checkpointer after the stream ends. 404 and 400 are raised before the stream starts; later failures become an error event with the exception class only (e.g. OpenAIModelNotFoundError).
- Deviations from the contract: body reuses SendMessageIn (provider/model ignored); added X-Accel-Buffering and Cache-Control headers; nginx got proxy_http_version 1.1 and an empty Connection header (if you added them).
- How to test: curl -N against groq, fake, and a conversation with a bad model id (error event, then close); 404 on an unknown conversation.
- Known gaps: no cancel; no tool events; one shared checkpointer connection; reasoning tokens counted in output but not streamed; Groq deltas include markdown line-break spaces (UI should use markdown or pre-wrap); usage depends on a checkpointer read; a failed turn leaves the user message in history; create_conversation doesn't validate the model id against the provider's list; only stream_mode="messages" was tried ("updates" and "values" not compared).
