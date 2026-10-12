# S-011 Versioned prompt store and editor
Milestone: M2 Agents, tools, token control
Status: todo   <!-- todo | doing | done -->
Depends on: S-010

## Goal
Edit prompts in a proper editor, save versions, see diffs, roll back.

## Done when (runnable in 2 minutes)
1. Save v2; v1 still exists.
2. Diff v1 vs v2 shows the change.
3. An agent pinned to v1 keeps v1; "follow latest" uses v2.
4. The trace records prompt name and version.

## Backend tasks
- [ ] prompts table with versions and endpoints.
- [ ] Agents reference name + version or latest.
- [ ] Add prompt name and version to trace attributes.

## Frontend tasks
- [ ] Prompts page: list, Monaco editor, history, diff, rollback (mockup).

## Files to create or change
Imports and exports are design intent. Adjust when you build, and verify library names in current docs.

### Backend
| File | Does | Imports | Exports |
|---|---|---|---|
| `apps/api/alembic/versions/0005_prompts.py` | prompts table | alembic | upgrade(), downgrade() |
| `apps/api/app/db/models/prompt.py` | name, version, text, created_at | db.base | Prompt |
| `apps/api/app/services/prompts.py` | Save versions, resolve name + version or latest | db.session | save_prompt_version, get_prompt(name, version), list_versions(name) |
| `apps/api/app/routers/prompts.py` | Prompt endpoints incl. rollback (new version copying an old one) | services.prompts | router |
| `apps/api/app/db/models/agent.py (edit)` | prompt_name, prompt_version (nullable = latest) | sqlalchemy | Agent |
| `apps/api/app/services/chat.py (edit)` | Resolve prompt and set trace attributes | services.prompts, opentelemetry | send_message |

### Frontend
| File | Does | Imports | Exports |
|---|---|---|---|
| `apps/web/src/pages/PromptsPage.tsx` | List, edit, history | PromptEditor, VersionHistory | PromptsPage |
| `apps/web/src/components/PromptEditor.tsx` | Monaco editor with Save as new version | @monaco-editor/react | PromptEditor |
| `apps/web/src/components/VersionHistory.tsx` | Versions list with rollback | hooks.usePromptVersions | VersionHistory |
| `apps/web/src/components/DiffView.tsx` | Side-by-side diff | Monaco diff editor | DiffView |

## Contract
```
Write this before building (endpoint, request, response example, errors).
```

## Out of scope
Prompt evals, templating beyond {{name}}.

## Log (fill in as you go)
- Built:
- Deviations from the contract:
- How to test:
- Known gaps:
