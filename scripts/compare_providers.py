"""S-004: Sends one prompt through every configured provider
Imports: llm.factory
Exports: (script)
"""
"""Send one prompt through every available provider.
Usage: docker compose exec api python /app/scripts/compare_providers.py [--prompt ...] [--only groq,fake]
       [--model groq=openai/gpt-oss-120b]
"""
import argparse
import sys
import time
from pathlib import Path

here = Path(__file__).resolve().parent
for cand in (here.parent, here.parent / "apps" / "api"):   # container, or repo checkout
    if (cand / "app").is_dir():
        sys.path.insert(0, str(cand))

from app.llm.factory import build_chat_model  # noqa: E402
from app.llm.providers import FAKE_MODEL_ID, PROVIDERS  # noqa: E402
from app.tracing import setup_script_tracing  # noqa: E402

# Defaults may go stale. Override with --model, using ids from GET /api/models.
DEFAULT_MODELS = {
    "groq": "openai/gpt-oss-120b",
    "openrouter": "meta-llama/llama-3.3-70b-instruct:free",
    "nvidia": "meta/llama-3.3-70b-instruct",
    "fake": FAKE_MODEL_ID,
}

ap = argparse.ArgumentParser()
ap.add_argument("--prompt", default="In one sentence, what is retrieval-augmented generation?")
ap.add_argument("--only", default="")
ap.add_argument("--model", action="append", default=[], help="provider=model")
args = ap.parse_args()

models = {**DEFAULT_MODELS, **dict(m.split("=", 1) for m in args.model)}
only = {s for s in args.only.split(",") if s}
tracer_provider = setup_script_tracing()

for name, p in PROVIDERS.items():
    if only and name not in only:
        continue
    if not p.available:
        print(f"[{name}] skipped (no key)")
        continue
    try:
        llm = build_chat_model(name, models[name], temperature=0) if name != "fake" \
            else build_chat_model("fake", models[name])
        t0 = time.perf_counter()
        msg = llm.invoke(args.prompt)
        dt = time.perf_counter() - t0
        print(f"[{name}] {models[name]}  {dt:.2f}s  usage={msg.usage_metadata}\n  {msg.content[:300]}\n")
    except Exception as e:
        print(f"[{name}] FAILED: {type(e).__name__}: {str(e)[:200]}\n")

tracer_provider.force_flush()