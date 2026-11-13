"""Fail-closed readiness checks for Japanese narration across all genres."""
from __future__ import annotations
import shutil
import subprocess

def check_offline_japanese_voice() -> dict:
    """A binary alone is not proof that a Japanese voice/model is installed."""
    piper = shutil.which("piper")
    espeak = shutil.which("espeak-ng")
    return {"ready": False, "engine_candidates": [x for x in (piper, espeak) if x],
            "reason": "Japanese model/voice and spoken output not verified",
            "publication_approved": False}

def assert_narrated_video(audio_verified: bool, japanese_verified: bool,
                          captions_synced: bool, rights_approved: bool,
                          employee_approved: bool) -> None:
    checks = (audio_verified, japanese_verified, captions_synced,
              rights_approved, employee_approved)
    if not all(checks):
        raise ValueError("PUBLICATION_NOT_APPROVED: missing verified gates")
