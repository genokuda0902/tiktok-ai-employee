"""Fail-closed publication gate for any of the ten TikTok genres.

Never infer Japanese speech or caption synchronization from the presence of
an audio stream or SRT file alone.
"""
def assess(manifest):
    required = ("video_decodes", "resolution_ok", "japanese_speech_verified",
                "captions_synced_verified", "assets_approved",
                "human_quality_approved")
    missing = [name for name in required if manifest.get(name) is not True]
    return {"posting_allowed": not missing,
            "status": "APPROVED_FOR_MANUAL_POST" if not missing else "PUBLICATION_NOT_APPROVED",
            "failed_checks": missing}
