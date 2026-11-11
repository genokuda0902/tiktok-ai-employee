"""Fail-closed publication gate for any of the ten content genres."""
import json
from pathlib import Path

REQUIRED = ("narration_verified", "captions_synced", "approved")

def publication_ready(manifest):
    return all(manifest.get(key) is True for key in REQUIRED)

def check(path):
    data = json.loads(Path(path).read_text(encoding="utf-8"))
    return publication_ready(data)

if __name__ == "__main__":
    import sys
    if not check(sys.argv[1]):
        raise SystemExit("PUBLICATION_NOT_APPROVED")
