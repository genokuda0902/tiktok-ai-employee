"""Cross-genre fail-closed review manifest validation. No external dependencies."""
from pathlib import Path
import json

REQUIRED = ("status", "posting_allowed", "audio", "captions", "assets", "scenes")

def validate(manifest):
    if not isinstance(manifest, dict) or any(k not in manifest for k in REQUIRED):
        return False
    if manifest["posting_allowed"] is not False or manifest["status"] != "REVIEW_ONLY":
        return False
    if manifest["audio"] != "absent":
        return False
    return manifest["scenes"] == 4 and manifest["assets"] == "original synthetic graphics only"

def load_and_validate(path):
    return validate(json.loads(Path(path).read_text(encoding="utf-8")))
