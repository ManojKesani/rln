# Git and Three-Hat Cheat Sheet (Trillian)

## 1. One-time setup

```bash
git config --global user.name "Your Name"
git config --global user.email "you@example.com"
git config --global init.defaultBranch main
```

`.gitignore` (create before the first commit):

```bash
cat > .gitignore <<'EOF'
.env
.venv/
__pycache__/
node_modules/
data/raw/
*.pyc
.DS_Store
EOF
```

## 2. First commit (docs, mockup, slices)

```bash
unzip workbench-repo-docs.zip -d .            # docs, mockup, S-001
unzip -o trillian-slices.zip -d slices/       # all slice files
git status
git add -A
git commit -m "docs: planning docs, mockup, all slice files"
git tag m0-start
```

Connect to GitHub (optional, for backup). Create an empty repo there first:

```bash
git remote add origin git@github.com:YOURNAME/trillian.git
git push -u origin main
git push --tags
```

## 3. The three-hat loop for one slice

| Step | Hat | Where | What you do | Status line | Git |
|---|---|---|---|---|---|
| 1 | **PM chat** | New PM chat | Paste the pack and `prompts/pm-spec.md`. Save the output into the slice file | `spec` | `git switch -c s-00X-name` |
| 2 | **You** | Slice file | Read the contract and edit it if it doesn't fit. Bump `Contract version` if you change it | `contract-agreed` | `git commit -m "S-00X: agree contract"` |
| 3 | **Backend** | Code | Build it. Test via `/docs`, curl, or a script. Check the trace in Phoenix. Fill in Backend notes | `backend-done` | `git commit -m "S-00X: backend"` |
| 4 | **Frontend chat** | New frontend chat | Paste the pack and `prompts/frontend-build.md`. Run the result and fix it. Fill in Frontend notes | `frontend-done` | `git commit -m "S-00X: frontend"` |
| 5 | **PM chat (fresh)** | New PM chat | Paste the pack, your results, and `prompts/pm-acceptance.md` | `accepted`, or back to 3 or 4 | See below |
| 6 | **You** | Repo | Move the slice to `archive/` with a 5-line summary. Update `STATUS.md` and `DEVLOG.md` | | `git commit -m "S-00X: accepted"` |

On acceptance:

```bash
git switch main
git merge --no-ff s-00X-name -m "S-00X accepted"
git tag m1-s00X
git push && git push --tags
git branch -d s-00X-name
```

Slices with no UI skip step 4. S-007 has no new backend, so it skips step 3.

### Status line at a glance

```
spec -> contract-agreed -> backend-done -> frontend-done -> accepted
 PM         you              you            frontend         PM
```

Whoever's name is under the next arrow has the next move. Write it in `Owner now`.

## 4. What to paste into each chat

| Chat | Paste |
|---|---|
| **PM, spec** | `PROJECT.md`, `ROLES.md` (PM card), `BACKLOG.md`, `STATUS.md` |
| **Frontend** | `frontend-rules.md`, the slice file, the relevant `openapi.json` excerpt, the name of the mockup page |
| **PM, acceptance** | `PROJECT.md`, the PM card, the slice file, your results for each "done when" step |

Aim for 2-3k tokens per chat. Never paste the whole codebase.

## 5. Rules that stop things from drifting

- **One slice in flight.** Don't start the next until this one is accepted or parked.
- **Contract before code.** Changing it means bumping the version and telling the frontend chat.
- **Backend before frontend.** The API schema is the handoff.
- **Questions go in the slice file** under Open questions. Never let an LLM guess silently.
- **The PM judges only against "done when".** New ideas go to the parked list in `BACKLOG.md`.
- **One chat per role per slice.** Start a new one when it gets long or confused.
- **Every chat starts with a two-sentence restatement and ends with assumptions.**

## 6. When something goes wrong

| Situation | Do this |
|---|---|
| Chat gets long or confused | `prompts/handoff.md`, paste the note into the slice file, open a fresh chat |
| Stuck debugging | `prompts/debug-restart.md` in a new chat |
| PM and frontend disagree | Put both positions in Open questions, decide yourself, add a line to `DECISIONS.md` |
| Backend response changed | Bump the contract version, regenerate `openapi.json`, re-tell the frontend chat |
| AI broke a file | `git restore --source=HEAD path/to/file` |
| Slice too big | Split it, update `BACKLOG.md`, number the new one |

## 7. Session start and end

**Start:** read `STATUS.md` and the slice file, run `make smoke`, then open the chat for whichever hat acts next.

```bash
git status
git log --oneline -5
git switch <your-slice-branch>
```

**End:** commit, update the slice's Status and notes, set the next action in `STATUS.md`, and add a few lines to `DEVLOG.md`.

## 8. Daily git loop

```bash
git switch -c s-001-compose-stack     # start a slice
git status                            # what changed
git diff                              # review before staging
git add -A                            # or: git add path/to/file
git commit -m "S-001: add postgres and redis to compose"
git push -u origin s-001-compose-stack   # first push of a branch; later just: git push
```

### Commit message pattern

```
S-004: add model factory with fake provider
S-004: fix groq base_url
docs: update STATUS after S-004
```

The prefix is the slice id (or `docs`, `chore`, `fix`), then a short sentence about what changed.

## 9. Looking around

```bash
git log --oneline -10                 # last ten commits
git log --oneline --graph --all       # branches drawn as a tree
git show HEAD                         # what the last commit changed
git diff main..s-004-model-factory    # compare branches
git tag                               # list tags
git branch                            # list branches
```

## 10. Undoing things

```bash
git restore path/to/file              # discard unstaged changes in a file
git restore --staged path/to/file     # unstage a file, keep the changes
git restore --source=HEAD path/to/file   # get the last committed version back
git commit --amend -m "new message"   # fix the last commit message (only if not pushed)
git revert <commit>                   # new commit that undoes an old one (safe)
git reset --hard <commit>             # throw away everything after a commit (destructive)
git switch -c rescue-branch           # save your current state before something risky
```

## 11. Pausing mid-work

```bash
git stash push -m "wip: sse endpoint"   # set work aside
git stash list
git stash pop                           # bring it back
```

Alternatively, commit with `wip:` at the end of a session. The slice file notes explain where you stopped.

## 12. Tags

- **Per slice:** `m0-s001`, `m1-s005`
- **Per milestone:** `m1-chat-works`

Return to a good state at any time:

```bash
git switch --detach m1-chat-works          # look around
git switch -c fix-from-m1 m1-chat-works    # branch from it
```

## 13. Habits worth keeping

- Run `git status` and `git diff` before every commit, and read what the AI changed.
- Commit at every handoff: after the contract is agreed, after the backend works, and after the frontend works.