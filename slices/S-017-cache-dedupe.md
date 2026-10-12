# S-017 Embedding cache and dedupe
Milestone: M3 Ingestion and chunk viewer
Status: todo   <!-- todo | doing | done -->
Depends on: S-016

## Goal
Re-ingesting does almost no work and duplicates are flagged.

## Done when (runnable in 2 minutes)
1. Re-ingest the same corpus: cache hits near 100% and much faster.
2. Exact duplicates flagged.
3. Near-duplicates flagged.
4. Use your self-made duplicate files.

## Backend tasks
- [ ] Chunk hash and embedding cache keyed by hash + model.
- [ ] Exact and near-duplicate detection.
- [ ] Flags stored on chunks.

## Frontend tasks
- [ ] Dup and cache-hit flags in the chunk table and stats.

## Files to create or change
Imports and exports are design intent. Adjust when you build, and verify library names in current docs.

### Backend
| File | Does | Imports | Exports |
|---|---|---|---|
| `apps/api/alembic/versions/0010_cache_flags.py` | embedding_cache table, chunks.hash and chunks.flag | alembic | upgrade(), downgrade() |
| `apps/api/app/db/models/embedding_cache.py` | Cache table: chunk hash, embedding model, vector | db.base, pgvector.sqlalchemy.Vector | EmbeddingCacheRow |
| `apps/api/app/ingestion/hashing.py` | Normalized chunk hash | hashlib | chunk_hash(text) |
| `apps/api/app/ingestion/cache.py` | Embedding cache keyed by (hash, model) | db.session | EmbeddingCache.get_many, put_many |
| `apps/api/app/ingestion/dedupe.py` | Exact and near-duplicate detection | datasketch or own MinHash (decide) | find_exact_duplicates, find_near_duplicates |
| `apps/api/app/ingestion/pipeline.py (edit)` | Use cache and dedupe, record flags and stats | cache, dedupe | ingest_file |

### Frontend
| File | Does | Imports | Exports |
|---|---|---|---|
| `apps/web/src/components/ChunkList.tsx (edit)` | Show duplicate and cache-hit flags | (props) | ChunkList |
| `apps/web/src/components/IngestStats.tsx` | Cache hit rate and duplicate counts | (props) | IngestStats |

## Contract
```
Write this before building (endpoint, request, response example, errors).
```

## Out of scope
Cross-collection dedupe.

## Log (fill in as you go)
- Built:
- Deviations from the contract:
- How to test:
- Known gaps:
