# S-018 Ingestion profiles and collection versions
Milestone: M3 Ingestion and chunk viewer
Status: todo   <!-- todo | doing | done -->
Depends on: S-017

## Goal
Save named ingestion settings and compare resulting collections.

## Done when (runnable in 2 minutes)
1. Save a profile and rerun it on another dataset.
2. Versions table shows profile, chunk count, time, cache hits.
3. Compare two versions side by side.

## Backend tasks
- [ ] ingestion_profiles table, versioned.
- [ ] Collection stores profile id.
- [ ] Compare endpoint.

## Frontend tasks
- [ ] Profile name, save and load on the Ingestion page; versions table; compare view.

## Files to create or change
Imports and exports are design intent. Adjust when you build, and verify library names in current docs.

### Backend
| File | Does | Imports | Exports |
|---|---|---|---|
| `apps/api/alembic/versions/0011_ingestion_profiles.py` | ingestion_profiles; collections.profile_id | alembic | upgrade(), downgrade() |
| `apps/api/app/db/models/ingestion_profile.py` | name, version, settings JSON | db.base | IngestionProfile |
| `apps/api/app/services/profiles.py` | Save versions, load, compare collections | db.session | save_profile, get_profile, compare_collections |
| `apps/api/app/routers/ingestion.py (edit)` | Profile endpoints and GET /api/collections/compare | services.profiles | router |

### Frontend
| File | Does | Imports | Exports |
|---|---|---|---|
| `apps/web/src/components/ProfileForm.tsx` | Settings form with name, save, load | hooks.useProfiles | ProfileForm |
| `apps/web/src/components/VersionsTable.tsx` | Collection versions table | (props) | VersionsTable |
| `apps/web/src/components/CompareView.tsx` | Two versions side by side | (props) | CompareView |

## Contract
```
Write this before building (endpoint, request, response example, errors).
```

## Out of scope
Retrieval profiles.

## Log (fill in as you go)
- Built:
- Deviations from the contract:
- How to test:
- Known gaps:
