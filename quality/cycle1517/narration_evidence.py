"""Fail-closed, genre-independent narration evidence gate. Stdlib only."""
import json
from pathlib import Path

def check(manifest):
    required = ("narration_language", "narration_verified", "caption_sync_verified",
                "asset_rights_approved", "human_quality_approved")
    missing = [k for k in required if k not in manifest]
    problems = ["missing:" + k for k in missing]
    if manifest.get("narration_language") != "ja":
        problems.append("Japanese narration not evidenced")
    for k in required[1:]:
        if manifest.get(k) is not True:
            problems.append(k + " not verified")
    if manifest.get("posting_allowed") is not False:
        problems.append("review pipeline must keep posting disabled")
    return {"passed": not problems, "issues": problems, "posting_allowed": False}

if __name__ == "__main__":
    import sys
    result = check(json.loads(Path(sys.argv[1]).read_text(encoding="utf-8")))
    print(json.dumps(result, ensure_ascii=False))
    raise SystemExit(0 if result["passed"] else 1)
