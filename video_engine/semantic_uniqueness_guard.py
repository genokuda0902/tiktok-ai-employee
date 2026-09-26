"""Fail-closed semantic uniqueness guard for image-first TikTok stories.

Prevents a nominal 30-45s manifest from passing when it merely loops the same
visual/copy/narration beat. Zero-cost and genre-independent.
"""
from __future__ import annotations
from collections import Counter
from .unified_story_manifest import StoryManifest

def _norm(value: str) -> str:
    return "".join(value.lower().split())

def validate_semantic_uniqueness(manifest: StoryManifest, max_duplicate_ratio: float = 0.20) -> dict:
    manifest.validate()
    if not 0.0 <= max_duplicate_ratio <= 0.25:
        raise ValueError("max_duplicate_ratio outside safe range")
    fields = {
        "image_copy": [_norm(c.image_copy) for c in manifest.cuts],
        "narration": [_norm(c.narration) for c in manifest.cuts],
        "caption": [_norm(c.caption) for c in manifest.cuts],
    }
    result = {}
    for name, values in fields.items():
        counts = Counter(values)
        duplicate_count = sum(n - 1 for n in counts.values() if n > 1)
        ratio = duplicate_count / len(values)
        if ratio > max_duplicate_ratio:
            raise ValueError(f"{name} repeats too much: {ratio:.3f}")
        result[name] = {"unique": len(counts), "duplicate_ratio": round(ratio, 3)}
    return result

def release_contract() -> dict:
    return {
        "zero_cost": True,
        "genre_independent": True,
        "reject_looped_story": True,
        "human_approval_required": True,
        "manual_post_only": True,
        "auto_post": False,
    }
