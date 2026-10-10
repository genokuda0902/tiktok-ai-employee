"""Reusable, fail-closed execution-evidence contract for review-only videos."""
from __future__ import annotations
import hashlib
import json
import subprocess
import sys
from pathlib import Path

SOURCE_CODE = "print(sum([12, 9, 14]))"
EXPECTED_STDOUT = "35"

def generate_evidence(destination: str | Path) -> dict:
    """Run real local Python computation; record stdout and provenance."""
    actual = subprocess.check_output(
        [sys.executable, "-c", SOURCE_CODE], text=True, timeout=10
    ).strip()
    if actual != EXPECTED_STDOUT:
        raise RuntimeError("FAIL CLOSED: arithmetic evidence mismatch")
    payload = {
        "source": "LOCAL_PYTHON_EXECUTION",
        "script": SOURCE_CODE,
        "input_values": [12, 9, 14],
        "observed_stdout": actual,
        "sha256_script": hashlib.sha256(SOURCE_CODE.encode()).hexdigest(),
        "ui_representation": "SYNTHETIC_RECONSTRUCTION",
        "rights": "ORIGINAL_SYNTHETIC",
        "privacy": "NO_REAL_PERSONAL_DATA",
        "human_approved": False,
        "publication": "NOT_APPROVED",
    }
    path = Path(destination)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    return payload

def validate_review_manifest(manifest: dict) -> None:
    """Never promote technical render success to content approval."""
    if manifest.get("rights") != "ORIGINAL_SYNTHETIC":
        raise ValueError("Unapproved or unknown asset rights")
    if manifest.get("privacy") != "NO_REAL_PERSONAL_DATA":
        raise ValueError("Privacy verification absent")
    if manifest.get("human_approved") is not False:
        raise ValueError("Human approval must not be assumed")
    if manifest.get("publication") != "NOT_APPROVED":
        raise ValueError("Review-only asset cannot be marked approved")
    if manifest.get("narration_verified") is not False:
        raise ValueError("No real Japanese narration has been verified")
    if manifest.get("captions_synced") is not False:
        raise ValueError("No measured narration/caption sync has been verified")
    if manifest.get("auto_post") is not False:
        raise ValueError("Automatic posting is forbidden")

if __name__ == "__main__":
    print(json.dumps(generate_evidence("output/cycle472/evidence.json"), ensure_ascii=False))
