# S-032 Image ingestion with CLIP
Milestone: M7 Multimodal
Status: todo   <!-- todo | doing | done -->
Depends on: S-028

## Goal
Ingest images and embed them in an image-text space.

## Done when (runnable in 2 minutes)
1. A Flickr8k subset (200-1000 images) embeds on CPU.
2. Images are stored with caption and source.
3. The collection records the image embedding model.

## Backend tasks
- [ ] CLIP embedder.
- [ ] Image ingestion path and storage.

## Frontend tasks
- [ ] Image upload on the Ingestion page; thumbnails in the chunk viewer.

## Files to create or change
Imports and exports are design intent. Adjust when you build, and verify library names in current docs.

### Backend
| File | Does | Imports | Exports |
|---|---|---|---|
| `scripts/download_flickr8k.py` | Downloads a subset into data/raw | httpx or datasets | (script) |
| `apps/api/app/multimodal/clip.py` | Image and text embeddings in one space | open_clip or transformers CLIP | ClipEmbedder.embed_images, embed_texts |
| `apps/api/app/ingestion/loaders.py (edit)` | Image loader | PIL | load_image |
| `apps/api/app/db/models/chunk.py (edit)` | modality, asset_path | sqlalchemy | Chunk |
| `apps/api/app/ingestion/pipeline.py (edit)` | Image ingestion path | multimodal.clip | ingest_file |

### Frontend
| File | Does | Imports | Exports |
|---|---|---|---|
| `apps/web/src/components/UploadBox.tsx (edit)` | Accept images | (props) | UploadBox |
| `apps/web/src/components/ChunkList.tsx (edit)` | Show thumbnails | (props) | ChunkList |

## Contract
```
Write this before building (endpoint, request, response example, errors).
```

## Out of scope
PDFs, VLM answering.

## Notes
Optional one-afternoon prototype earlier.

## Log (fill in as you go)
- Built:
- Deviations from the contract:
- How to test:
- Known gaps:
