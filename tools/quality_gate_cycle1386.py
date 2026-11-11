"""Fail-closed QA for review-only video manifests. No publishing side effects."""
import json
from pathlib import Path

REQUIRED = ("narration_verified", "subtitle_sync_verified", "posting_allowed", "manual_approval_required", "source")

def evaluate(manifest):
    missing = [key for key in REQUIRED if key not in manifest]
    if missing:
        return False, "missing: " + ", ".join(missing)
    if manifest["posting_allowed"] is not False:
        return False, "posting_allowed must remain false pending explicit approval"
    if manifest["manual_approval_required"] is not True:
        return False, "human approval must be required"
    if manifest["narration_verified"] is not True:
        return False, "Japanese narration not verified"
    if manifest["subtitle_sync_verified"] is not True:
        return False, "speech-synchronized subtitles not verified"
    return True, "technical checks only; human approval still required"

if __name__ == "__main__":
    import sys
    data = json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))
    passed, reason = evaluate(data)
    print(("PASS" if passed else "BLOCKED") + ": " + reason)
    sys.exit(0 if passed else 1)
