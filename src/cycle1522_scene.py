"""Cycle1522 review-only scene timing and publication gate (no external media)."""
SCENES = [
    (0, 3, "合計を手計算していませんか？"),
    (3, 6, "セルに数式を入力"),
    (6, 9, "Enterで結果が出る"),
    (9, 12, "同じ作業を短縮"),
]
PUBLICATION_APPROVED = False

def scene_at(seconds):
    if not 0 <= seconds < 12:
        raise ValueError("outside clip")
    return next(i for i, (start, end, _) in enumerate(SCENES)
                if start <= seconds < end)

def publication_allowed(japanese_voice_verified=False,
                        subtitles_synced=False, assets_approved=False,
                        human_approved=False):
    return bool(PUBLICATION_APPROVED and japanese_voice_verified
                and subtitles_synced and assets_approved and human_approved)
