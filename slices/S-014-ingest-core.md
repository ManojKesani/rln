# S-014 Upload, chunk, embed, store
Milestone: M3 Ingestion and chunk viewer
Status: todo   <!-- todo | doing | done -->
Depends on: S-013

## Goal
Upload a file and get searchable chunks in a collection.

## Done when (runnable in 2 minutes)
1. Upload a text file; chunks appear in pgvector.
2. The collection records embedding model and dimension.
3. Each chunk stores source, offsets and fetch date.
4. Another embedding model creates a new collection.

## Backend tasks
- [ ] collections, documents, chunks tables.
- [ ] Loader, recursive chunker, local embedder.
- [ ] Insert vectors into pgvector.
- [ ] Upload endpoint.

## Frontend tasks
- [ ] Ingestion page basics: upload box, collection list, chunk counts.

## Files to create or change
Imports and exports are design intent. Adjust when you build, and verify library names in current docs.

### Backend
| File | Does | Imports | Exports |
|---|---|---|---|
| `apps/api/alembic/versions/0008_collections_chunks.py` | CREATE EXTENSION vector; collections, documents, chunks | alembic, pgvector | upgrade(), downgrade() |
| `apps/api/app/db/models/collection.py` | name, embedding_model, dim, created_at | db.base | Collection |
| `apps/api/app/db/models/document.py` | collection_id, source, fetched_at, raw_path | db.base | Document |
| `apps/api/app/db/models/chunk.py` | document_id, text, start, end, embedding (vector) | pgvector.sqlalchemy.Vector | Chunk |
| `apps/api/app/ingestion/loaders.py` | Reads a text file into text + metadata | pathlib | load_text(path) |
| `apps/api/app/ingestion/chunkers.py` | Recursive chunking that keeps offsets | (none) | ChunkSpan, recursive_chunk(text, size, overlap) |
| `apps/api/app/ingestion/embedders.py` | Local embedding models | sentence_transformers | Embedder, get_embedder(name) |
| `apps/api/app/ingestion/pipeline.py` | load -> chunk -> embed -> insert | loaders, chunkers, embedders, db.session | ingest_file(path, collection_id) |
| `apps/api/app/services/collections.py` | Create/list collections | db.models.collection | create_collection, list_collections |
| `apps/api/app/schemas/ingestion.py` | Models for upload and collections | pydantic | CollectionOut, UploadResult |
| `apps/api/app/routers/ingestion.py` | POST /api/ingest/upload, GET /api/collections | services.collections, ingestion.pipeline | router |

### Frontend
| File | Does | Imports | Exports |
|---|---|---|---|
| `apps/web/src/pages/IngestionPage.tsx` | Upload box and collection list | UploadBox, CollectionList | IngestionPage |
| `apps/web/src/components/UploadBox.tsx` | File drop and upload | hooks.useUpload | UploadBox |
| `apps/web/src/components/CollectionList.tsx` | Collections with chunk counts | hooks.useCollections | CollectionList |

## Contract
```
Write this before building (endpoint, request, response example, errors).
```

## Out of scope
Jobs, dedupe, PDFs.

## Notes
Local embeddings (bge-small or MiniLM).

## Log (fill in as you go)
- Built:
- Deviations from the contract:
- How to test:
- Known gaps:
