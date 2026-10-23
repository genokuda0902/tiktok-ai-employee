"""Genre-neutral review-only QA contract for the kinetic CTA."""
GENRES=("ai_productivity","trivia","cooking","beauty","finance","wellness","travel","product_demo","story","business")
SAFE=(70,165,885,1550)
FPS=30
OUTRO_FRAMES=94
def validate_manifest(manifest):
    for field,value in {
        "quality_approved":False,"publication_approved":False,
        "employee_approved":False,"publish_mode":"employee_manual_only",
        "source_rights":"unverified_review_only",
        "audio_rights":"unverified_review_only",
        "caption_kind":"scene_summary_not_verbatim_transcript"
    }.items():
        if manifest.get(field)!=value:
            raise ValueError("review-only safety gate: "+field)
    if manifest.get("genre_id") not in GENRES:
        raise ValueError("unsupported genre")
    if not (manifest.get("source_sha256") and len(manifest["source_sha256"])==64):
        raise ValueError("source checksum required")
    if len(manifest.get("headline",""))>16 or len(manifest.get("cta",""))>20:
        raise ValueError("text too long")
    return True
