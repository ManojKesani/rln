# STATUS
Last updated: (date)
Current milestone: M0 Foundation
Current slice: S-001 compose-stack (todo)
Last known good commit/tag: none yet

## Next action
`git switch -c s-001-compose-stack`, then `bash scripts/make-skeleton.sh 1`, then build the backend tasks in slices/S-001-compose-stack.md.

## In progress
- Nothing

## Known bugs
- none

## Open questions
- Confirm D-005 (Redis + Arq) or drop the worker and S-016's queue for now.
- Should the Models page (S-013) wait until after M4?
- S-001: should /health also check Phoenix? (default: no)
