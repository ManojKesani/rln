#!/usr/bin/env bash
# Create the new files listed in a slice's "Files to create or change" tables.
#   bash scripts/make-skeleton.sh 7            create files for S-007
#   bash scripts/make-skeleton.sh 7 --dry-run  show what would be created
#   bash scripts/make-skeleton.sh all          every slice (usually not what you want)
# Run from the repo root. Never overwrites a file. Rows marked (edit) are listed, not created.
# Each new file gets a header with what it does, its imports and exports, taken from the slice file.
set -euo pipefail
command -v python3 >/dev/null || { echo "python3 is required"; exit 1; }

python3 - "$@" <<'PY'
import sys, re, glob, os

args = sys.argv[1:]
dry = "--dry-run" in args
args = [a for a in args if a != "--dry-run"]
if len(args) != 1:
    sys.exit("usage: bash scripts/make-skeleton.sh <slice-number|all> [--dry-run]")

if args[0] == "all":
    slice_files = sorted(f for f in glob.glob("slices/S-*.md"))
else:
    try:
        n = int(args[0])
    except ValueError:
        sys.exit("slice must be a number like 7, or 'all'")
    slice_files = glob.glob(f"slices/S-{n:03d}-*.md")
    if not slice_files:
        sys.exit(f"no slice file found for S-{n:03d} in slices/")

ROW = re.compile(r"^\| `(.+?)` \| (.*?) \| (.*?) \| (.*?) \|$")

def header(path, sid, does, imp, exp):
    lines = [f"{sid}: {does}", f"Imports: {imp}", f"Exports: {exp}"]
    base = os.path.basename(path)
    ext = os.path.splitext(path)[1]
    if ext == ".py":
        return '"""' + "\n".join(lines) + '\n"""\n'
    if ext in (".ts", ".tsx", ".js", ".jsx", ".css"):
        return "/**\n" + "".join(f" * {l}\n" for l in lines) + " */\n"
    if ext in (".html",):
        return "<!--\n" + "".join(f"  {l}\n" for l in lines) + "-->\n"
    if ext == ".ini":
        return "".join(f"; {l}\n" for l in lines)
    if ext in (".yml", ".yaml", ".conf", ".sh", ".toml", ".example") or base in ("Dockerfile", "Makefile"):
        return "".join(f"# {l}\n" for l in lines)
    return ""   # .md, .json and anything else start empty

def expand(raw):
    """Split 'a/b.ini + c.py' into paths; flag edits, folders and scaffolds."""
    if "(edit)" in raw:
        return [], "edit"
    if "(scaffolded)" in raw or raw.rstrip().endswith("/"):
        return [], "scaffold"
    parts = [p.strip() for p in raw.split(" + ")]
    out = [parts[0]]
    for p in parts[1:]:
        out.append(os.path.join(os.path.dirname(parts[0]), p))
    return out, "new"

def ensure_packages(path, created):
    if not (path.startswith("apps/api/app/") or path.startswith("apps/api/tests/")):
        return
    top = "apps/api/app" if path.startswith("apps/api/app/") else "apps/api/tests"
    d = os.path.dirname(path)
    while d.startswith(top):
        init = os.path.join(d, "__init__.py")
        if not os.path.exists(init):
            if not dry:
                os.makedirs(d, exist_ok=True)
                open(init, "w").close()
            created.append(init + "  (package marker)")
        d = os.path.dirname(d)

for sf in slice_files:
    text = open(sf).read()
    sid = re.search(r"^# (S-\d+)", text, re.M).group(1)
    m = re.search(r"## Files to create or change(.*?)\n## Contract", text, re.S)
    if not m:
        print(f"{sid}: no Files section found, skipping"); continue
    created, existed, edits, scaffolds = [], [], [], []
    for line in m.group(1).splitlines():
        r = ROW.match(line)
        if not r:
            continue
        raw, does, imp, exp = r.groups()
        paths, kind = expand(raw)
        if kind == "edit":
            edits.append(raw.replace(" (edit)", "") + f"  - {does}"); continue
        if kind == "scaffold":
            scaffolds.append(f"{raw}  - {does}"); continue
        for p in paths:
            if os.path.exists(p):
                existed.append(p); continue
            if not dry:
                os.makedirs(os.path.dirname(p) or ".", exist_ok=True)
                open(p, "w").write(header(p, sid, does, imp, exp))
            created.append(p)
            ensure_packages(p, created)
    print(f"\n== {sid} {'(dry run) ' if dry else ''}==")
    for p in created:   print("  created ", p)
    for p in existed:   print("  exists  ", p)
    for p in scaffolds: print("  scaffold", p, " <- create this with its own tool FIRST (e.g. npm create vite@latest), then rerun this script")
    for p in edits:     print("  EDIT    ", p)
PY
