# Frontend rules (paste into any chat that touches apps/web)
- Stack: Vite, React, TypeScript (TSX), Tailwind, shadcn/ui, TanStack Query. react-router-dom for routing (add as a decision at S-007).
  No other libraries without asking.
- Dark mode by default, light via a toggle. Colors as CSS variables.
- API: use the typed client generated from openapi.json (openapi-typescript). Never invent endpoints or fields.
- Build only what the slice's Frontend tasks and Files table list. No extra features, animations or themes.
- Layout: apps/web/src/{api,lib,pages,components}. One component per file, props typed.
- Server data through TanStack Query hooks (api/hooks.ts); local UI state with useState. No global state library.
- Streaming chat uses SSE over fetch (lib/sse.ts) against /api.
- Ugly is fine; polish later. Show raw data where the mockup does (tables, scores, token counts).
- Visual spec: the Trillian mockup, https://claude.ai/artifact/3izZ2eZ9iUTXYP4Ju4MNjx
- End every reply with the assumptions you made.
