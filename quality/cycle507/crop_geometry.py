"""Cycle507 shared crop geometry; REVIEW ONLY. Never approves publication."""
GENRES = set("ai_work gadgets study travel cooking beauty home fitness history business".split())
CANVAS = (1080, 1920)
SOURCE_CROP_HEIGHT = 1512
CAPTION_LANE = (40, 1534, 1000, 160)
SAFE_BOTTOM = 1710

def validate(manifest):
    if manifest.get("genre") not in GENRES:
        raise ValueError("genre")
    if manifest.get("rights") != "original_procedural" or manifest.get("crop_reviewed") is not True:
        raise ValueError("source rights and manual crop review required")
    if manifest.get("publication") != "NOT_APPROVED" or manifest.get("human_review") != "HUMAN_REVIEW" or manifest.get("auto_post") is not False:
        raise ValueError("must remain review-only")
    if manifest.get("narration_status") != "NOT_AVAILABLE":
        raise ValueError("unverified narration")
    y = manifest.get("crop_y")
    if type(y) is not int or not 0 <= y <= 408:
        raise ValueError("crop y")
    overrides = manifest.get("crop_overrides", {})
    if not isinstance(overrides, dict):
        raise ValueError("crop overrides")
    for key, value in overrides.items():
        if key not in {str(i) for i in range(8)} or type(value) is not int or not 0 <= value <= 408:
            raise ValueError("unapproved crop override")
    if SOURCE_CROP_HEIGHT >= CAPTION_LANE[1] or CAPTION_LANE[1] + CAPTION_LANE[3] > SAFE_BOTTOM:
        raise ValueError("unsafe subtitle lane")
    return overrides

def crop_expression(manifest):
    overrides = validate(manifest)
    expr = str(manifest["crop_y"])
    for key, value in sorted(overrides.items(), reverse=True):
        index = int(key)
        if value != manifest["crop_y"]:
            expr = "if(between(t\\,%s\\,%s)\\,%s\\,%s)" % (index*2.5, (index+1)*2.5, value, expr)
    return expr
