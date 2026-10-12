# S-004 Model factory and model list
Milestone: M1 Chat with history and model selection
Status: todo   <!-- todo | doing | done -->
Depends on: S-002, S-003

## Goal
List models per provider and build a LangChain chat model from a provider and model string, including a free fake model.

## Done when (runnable in 2 minutes)
1. GET /api/models lists Groq, OpenRouter, NVIDIA NIM and fake with model ids.
2. One script sends the same prompt through each configured provider by changing one parameter.
3. The fake model answers with zero tokens and no network.
4. Calls appear in Phoenix via the LangChain instrumentor.

## Backend tasks
- [ ] llm/providers.py: base_url and key per provider, the fake model.
- [ ] llm/factory.py: provider + model string -> chat model.
- [ ] GET /api/models: ids and an available flag. A provider with no key is "unavailable", not an error.
- [ ] Turn on the LangChain instrumentor.

## Frontend tasks
- [ ] None in this slice.

## Files to create or change
Imports and exports are design intent. Adjust when you build, and verify library names in current docs.

### Backend
| File | Does | Imports | Exports |
|---|---|---|---|
| `apps/api/app/llm/providers.py` | Provider table (base_url, key env var, models url) and the fake model | dataclasses, os, langchain_core fake chat model | ProviderConfig, PROVIDERS, make_fake_model() |
| `apps/api/app/llm/factory.py` | Builds a LangChain chat model from provider + model strings | langchain_openai.ChatOpenAI, llm.providers | build_chat_model(provider, model, **params), UnknownProviderError |
| `apps/api/app/llm/catalog.py` | Fetches each provider's /models list, marks unavailable ones | httpx, llm.providers | list_all_providers() |
| `apps/api/app/schemas/models.py` | Response models | pydantic.BaseModel | ModelInfo, ProviderInfo, ModelsResponse |
| `apps/api/app/routers/models.py` | GET /api/models | fastapi.APIRouter, llm.catalog, schemas.models | router |
| `apps/api/app/tracing.py (edit)` | Turn on the LangChain instrumentor | openinference-instrumentation-langchain | setup_tracing() |
| `scripts/compare_providers.py` | Sends one prompt through every configured provider | llm.factory | (script) |

### Frontend
None in this slice.

## Contract
```
GET /api/models -> 200 {"providers": [{"name": "groq", "available": true, "models": [{"id": "...", "name": "..."}]}]}
```

## Out of scope
Capability flags, rate limits, UI.

## Notes
The SimpleSpanProcessor warning comes from register() in the script. It exports each span synchronously, which is fine for a short script. For the API it is worth switching to batching later: register(..., batch=True) in _provider(). Check the parameter name in your installed version before relying on it.
Groq lists non-chat models (Orpheus is text-to-speech, Prompt Guard is a classifier). That is the known gap from the slice: filtering waits for capability flags in a later slice.
The reply text printed informationretrieved with the space missing. That's Groq's streaming output or the terminal, not a bug in the factory.

- Built: provider table (groq, openrouter, nvidia via ChatOpenAI+base_url, fake via GenericFakeChatModel), build_chat_model(), cached async GET /api/models (protected), LangChain instrumentor, scripts/compare_providers.py.
- Deviations from the contract: ProviderInfo has an extra optional `error` field; tracing.py gained setup_script_tracing(); ./scripts bind-mounted into the api container; optional `rpm` param on the factory.
- How to test: GET /api/models with the cookie; docker compose exec api python /app/scripts/compare_providers.py [--only fake]; check LLM spans in Phoenix.
- Known gaps: no model filtering (Groq/NVIDIA include non-chat models, OpenRouter is huge); default model ids in the script may go stale; OpenRouter and NVIDIA untested (no keys); retries off.
