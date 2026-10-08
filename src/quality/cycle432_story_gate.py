"""Review-only four-beat storyboard quality contract for ten genres."""
BEAT_FRAMES = (18, 18, 18, 21)
def inspect_story(scenes, rights, is_fictional, publication, auto_post):
    errors = []
    if len(scenes) != 8:
        errors.append("SCENE_COUNT")
    for i, scene in enumerate(scenes):
        if not all(scene.get(k) for k in ("title", "before", "after", "tip")):
            errors.append("MISSING_SCENE_FIELD_%d" % i)
        captions = scene.get("captions", [])
        if len(captions) != 4 or any(not t or len(t) > 36 for t in captions):
            errors.append("BAD_CAPTION_%d" % i)
    if rights != "ORIGINAL_ONLY":
        errors.append("RIGHTS_UNVERIFIED")
    if is_fictional is not True:
        errors.append("FICTIONALITY_UNVERIFIED")
    if publication != "NOT_APPROVED" or auto_post is not False:
        errors.append("PUBLICATION_GUARD")
    if sum(BEAT_FRAMES) * 8 != 600:
        errors.append("TIMELINE")
    return {"technical_contract_pass": not errors, "errors": errors,
            "japanese_narration": "UNVERIFIED", "human_review_required": True,
            "publication": "NOT_APPROVED"}
