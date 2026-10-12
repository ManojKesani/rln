# Resuming Work Across Breaks and Dead Chats

A reusable playbook for any project built with AI assistants (Claude, ChatGPT, Gemini, Grok, etc.).

**Core principle: the repo is the memory, not the chat.**
Chats are disposable workers. Anything you would hate to lose goes into a file in the repo. If a chat dies or you take a two-day break, you lose nothing but scrollback.

---

## 1. The problem

- You work 3 days, leave for 2, and come back with no context.
- A chat runs out of tokens, or gets so long (code, errors, debugging back and forth) that quality degrades.
- Different AI tools each know only their own chat.

The fix is a small set of docs, two short rituals, and some chat hygiene.

---

## 2. The docs folder

Each file has one job.

| File | Contains | Changes |
|---|---|---|
| `PROJECT.md` | Goal, ranked priorities, cross-cutting rules, chosen stack | Rarely |
| `ARCHITECTURE.md` | Services, data flow, data model, folder layout, simple diagram | When structure changes |
| `DECISIONS.md` | One short paragraph per decision: what, why, what was rejected | Append-only |
| `STATUS.md` | Current milestone, done, in progress, next single action, known bugs, open questions | Every session |
| `DEVLOG.md` | Dated entries: what you tried, what broke, what you learned | Every session |
| `frontend-rules.md` | Stack and conventions to paste into any AI chat (if you rely on AI for code you can't write yourself) | Rarely |

`STATUS.md` matters most when you return after a break. Its key field is **"Next action"**: one concrete step, for example "wire the SSE endpoint to the chat view; backend works, test with curl first." Without it you spend the first hour working out where you were.

---

## 3. End-of-session ritual (5 minutes)

1. Get to a stable point and commit. The message should say what works and what doesn't.
2. Update `STATUS.md`: done, half-done, next action.
3. Add a few lines to `DEVLOG.md`, especially what surprised you.
4. Ask the AI in the current chat: "Summarize the decisions we made and the open problems for my status file." Paste the result in, edited by you.

Stopping mid-debug is fine. Write down the **symptom, what you already tried, and your best guess**. That note saves the most time later.

## 4. Start-of-session ritual (5 minutes)

1. Read `STATUS.md` and the last `DEVLOG.md` entry yourself. You need the context too, not just the AI.
2. Run the stack and a **smoke test** (a script or `make smoke` that exercises the main path, e.g. log in, send a message, check for a reply). It tells you in seconds whether yesterday's state still works.
3. Open a fresh AI chat with a **context pack** (section 6).

Never paste the whole codebase. Paste docs plus the two or three files you are changing.

---

## 5. Chat hygiene

- **One chat per task, not per project.** "Build the SSE endpoint" is a chat. When it is done, commit and close it.
- **Start a new chat when** it gets long, the AI forgets or contradicts earlier code, or you are on your third failed fix. Long debug threads degrade quality, not just capacity.
- **Restart debugging with a clean report** (section 7). Stating the problem clearly often solves it.
- **Make the AI write the handoff** before abandoning a long chat, and save it to the repo.
- **Treat AI code as a proposal.** Only what is committed counts. Nobody should have to remember "the version from the chat."
- If your tool has a Projects feature or equivalent, put the docs there as standing context. The repo copy stays the source of truth.

---

## 6. Context pack

A script (e.g. `make context`) that prints the following, in order, into one file to paste at the start of a new chat:

1. Fixed header: "You are helping me build this project. Follow the rules below. Propose changes as small diffs. Ask before adding libraries."
2. `PROJECT.md`
3. `ARCHITECTURE.md`
4. `frontend-rules.md` (only for frontend tasks)
5. `STATUS.md`
6. `git log --oneline -10` and the file tree
7. A hand-written section: **Today's task** plus the 2-3 relevant source files

Keep the pack under a few thousand tokens. If it grows beyond that, trim the docs.

---

## 7. Prompts to save

**Handoff prompt (for a dying chat):**

> Write a handoff note for this chat: current state of the code, decisions made and why, open problems with symptoms and what we tried, and the single next step. Keep it under 300 words so I can paste it into my status file.

**Debug-restart prompt:**

> Goal: ...
> Exact error: ...
> Relevant code: ...
> Already tried: ...
> What I expect to happen: ...

---

## 8. Templates

### `STATUS.md`

```markdown
# Status

**Last updated:** YYYY-MM-DD
**Current milestone:** 
**Last known good commit/tag:** (hash or tag)

## Next action (one concrete step)
> e.g. "Wire the SSE endpoint to the chat view. Backend works, test with curl first."

## Done
- [x] ...
- [ ] ...

## In progress / half-done
- What it is, which files, what state it's in

## Known bugs
- Symptom | what I tried | best guess

## Open questions
- Things I need to decide or look up

## How to verify the system works
- `make up && make smoke`
```

### `DEVLOG.md` entry

```markdown
## YYYY-MM-DD
**Goal for the session:**
**What I did:**
**What broke / surprised me:**
**What I learned:**
**Stopped at:** (state + the next action, mirrored in STATUS.md)
```

### `DECISIONS.md` entry

```markdown
## D-001: Short title of the decision
- **Date:**
- **Decision:**
- **Why:**
- **Rejected:** alternative (reason)
- **Revisit if:** condition that would change this
```

---

## 9. Repo habits that protect context

- **Small commits with descriptive messages.** `git log` becomes a readable history.
- **Tag milestones** (e.g. `m1-chat-works`) so you can always return to a known good state.
- **README with exact run commands** and a `.env.example` listing every needed variable. A `Makefile` with `make up`, `make smoke`, `make logs`, `make context` is even better.
- **Comment the why, not the what**, wherever a choice is non-obvious.
- **Keep a notes file for learning** (e.g. `drills/notes.md`) so lessons are not trapped in old chats.
- **Commit after every working piece**, so a bad AI rewrite is a one-command undo.

---

## 10. Why this also helps you

These docs serve you as much as the AI. A month later, when you need to explain why you chose a database or how a feature works, `DECISIONS.md` has the answer. Writing it down as you go is also the best way to learn from the project.

---

## Quick checklist

**Before closing a session**
- [ ] Stable point committed
- [ ] `STATUS.md` updated with a single next action
- [ ] `DEVLOG.md` entry added
- [ ] Decisions appended to `DECISIONS.md`

**Before starting a session**
- [ ] Read `STATUS.md` and the last devlog entry
- [ ] Stack up and smoke test passes
- [ ] Fresh chat opened with the context pack and today's task
