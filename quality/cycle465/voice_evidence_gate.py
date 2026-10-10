"""Reusable, fail-closed narration and proof gate for all ten genres.
Audio codec, waveform energy, and synthetic fixtures do not prove Japanese speech.
"""
def assess_readiness(beats, duration, *, voice_generated, human_listened, rights_verified):
    issues = []
    if not beats or len(beats) < 2:
        issues.append("SCENES_MISSING")
    else:
        if abs(beats[0].start) > 1e-6 or beats[0].end > 1.5:
            issues.append("HOOK_OUTSIDE_1_5S")
        if abs(beats[-1].end - duration) > 1e-6:
            issues.append("END_MISMATCH")
        if any(abs(a.end-b.start)>1e-6 for a,b in zip(beats,beats[1:])):
            issues.append("GAP_OR_OVERLAP")
        if any(not b.caption.strip() or not b.spoken.strip() for b in beats):
            issues.append("EMPTY_CAPTION_OR_SCRIPT")
    if not voice_generated:
        issues.append("JAPANESE_NARRATION_NOT_GENERATED")
    if not human_listened:
        issues.append("JAPANESE_PRONUNCIATION_NOT_REVIEWED")
    if not rights_verified:
        issues.append("RIGHTS_NOT_VERIFIED")
    fatal = {"SCENES_MISSING","HOOK_OUTSIDE_1_5S","END_MISMATCH","GAP_OR_OVERLAP","EMPTY_CAPTION_OR_SCRIPT"}
    return {"approved_for_review": bool(voice_generated and rights_verified and not fatal.intersection(issues)),
            "approved_for_publication": False, "issues": sorted(set(issues)), "human_review_required": True}
