"""Write openapi.json. Usage: python /app/scripts/export_openapi.py /out/openapi.json
Takes a path argument because importing app.main prints the Phoenix banner to stdout."""
import json
import sys
from pathlib import Path

here = Path(__file__).resolve().parent
for cand in (here.parent, here.parent / "apps" / "api"):
    if (cand / "app").is_dir():
        sys.path.insert(0, str(cand))

from app.main import app  # noqa: E402

Path(sys.argv[1]).write_text(json.dumps(app.openapi(), indent=2))
print("wrote", sys.argv[1])