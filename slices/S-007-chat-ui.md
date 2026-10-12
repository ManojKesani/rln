# S-007 Chat UI with conversation list
Milestone: M1 Chat with history and model selection
Status: todo   <!-- todo | doing | done -->
Depends on: S-006

## Goal
Open the app, log in, see conversations, start new ones, and chat with streaming replies.

## Done when (runnable in 2 minutes)
1. Login page works and redirects to chat.
2. Sidebar lists conversations; clicking loads history.
3. New chat, send a message, tokens stream in.
4. Refresh keeps the conversation.

## Backend tasks
- [ ] Make sure openapi.json is current and cookies work through nginx.
- [ ] Fix any contract gaps the UI finds.

## Frontend tasks
- [ ] Scaffold the app with `npm create vite@latest` (check the current docs), then Tailwind, shadcn/ui, TanStack Query.
- [ ] Generate the typed API client from openapi.json.
- [ ] Login page and Chat page (sidebar, messages, streaming via fetch stream), following the Chat page of the mockup.
- [ ] nginx serves the build.

## Files to create or change
Imports and exports are design intent. Adjust when you build, and verify library names in current docs.

### Backend
| File | Does | Imports | Exports |
|---|---|---|---|
| `scripts/export_openapi.py` | Writes openapi.json from the FastAPI app | app.main.app, json | (script) |
| `Makefile (edit)` | Add openapi target | (none) | make openapi |

### Frontend
| File | Does | Imports | Exports |
|---|---|---|---|
| `apps/web/ (scaffolded)` | package.json, vite.config.ts (dev proxy /api), Tailwind and shadcn config | npm create vite@latest, tailwind, shadcn/ui, @tanstack/react-query, react-router-dom | (project) |
| `apps/web/src/api/schema.d.ts` | Types generated from openapi.json | openapi-typescript | paths, components |
| `apps/web/src/api/client.ts` | Thin fetch wrapper with credentials included | schema.d.ts | api.get, api.post |
| `apps/web/src/api/hooks.ts` | TanStack Query hooks | @tanstack/react-query, client | useLogin, useMe, useConversations, useMessages, useCreateConversation |
| `apps/web/src/lib/sse.ts` | Reads a streaming POST and calls handlers per event | fetch, ReadableStream | streamChat(id, content, handlers) |
| `apps/web/src/main.tsx` | Mounts the app with QueryClientProvider and router | react-dom, App | (entry) |
| `apps/web/src/App.tsx` | Routes: /login and / | react-router-dom, pages, RequireAuth | App |
| `apps/web/src/components/RequireAuth.tsx` | Redirects to /login if useMe fails | hooks.useMe | RequireAuth |
| `apps/web/src/pages/LoginPage.tsx` | Login form | hooks.useLogin | LoginPage |
| `apps/web/src/pages/ChatPage.tsx` | Sidebar plus chat view | ConversationList, MessageList, ChatInput, lib/sse | ChatPage |
| `apps/web/src/components/ConversationList.tsx` | Lists conversations, New chat button | hooks.useConversations | ConversationList |
| `apps/web/src/components/MessageList.tsx` | Renders messages, including the one streaming | (props) | MessageList |
| `apps/web/src/components/ChatInput.tsx` | Text box and send | (props) | ChatInput |
| `apps/web/Dockerfile` | Builds the app, serves it with nginx | node, nginx | image (replaces web-placeholder in compose) |

## Contract
```
No new endpoints.
```

## Out of scope
Agents, collection picker, citations, token badge.

## Notes
Scaffold apps/web with Vite first (npm create vite@latest, check the current docs), then run `bash scripts/make-skeleton.sh 7`. The script never overwrites existing files.
Use only endpoints from S-002, S-005, S-006.

## Log (fill in as you go)
- Built: Vite + React + TS app in apps/web. Login page, RequireAuth guard, chat page with conversation sidebar, provider/model selects for new chats, streaming replies via a fetch-based SSE reader (lib/sse.ts), usage line under each reply. Typed client generated from openapi.json (make openapi). Web image: node build stage, then nginx serving dist/ with SPA fallback; compose `web` service now builds it.
- Deviations from the contract: none on the API. shadcn/ui was not initialised (no components needed yet); useModels hook added for the New chat selects; light/dark toggle added though not in the Files table; selected conversation kept in the URL as ?c=<id>.
- How to test: make up, open localhost:8080, log in, new chat on fake/fake-echo, send a message, F5. Dev loop: npm run dev in apps/web (proxy to 8080).
- Known gaps: no logout button; no cancel; no markdown rendering; theme doesn't persist; a failed turn leaves the user message in history; model selects apply only to new chats; SSE event types are hand-written; shadcn deferred.
