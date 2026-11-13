"""Fail closed when the video renderer or narration is not reproducible."""
from pathlib import Path

def publication_ready(meta: dict, renderer_path: str) -> bool:
    required = ('japanese_narration_verified', 'captions_synced', 'assets_licensed', 'employee_approved', 'decode_passed')
    return Path(renderer_path).is_file() and all(meta.get(k) is True for k in required)
