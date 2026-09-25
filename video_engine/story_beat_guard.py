"""Fail-closed narrative beat guard for 8-12 cut image-first stories."""
REQUIRED_ROLES = ("hook", "problem", "demo", "result", "cta")
ALLOWED_ROLES = {"hook","problem","setup","demo","process","result","before","after","proof","application","summary","cta"}

def validate_story_beats(cuts, min_unique_roles=7):
    if not 8 <= len(cuts) <= 12:
        raise ValueError("story must contain 8-12 cuts")
    roles=[]; seen=set()
    for i, cut in enumerate(cuts):
        role=str(cut.get("role", "")).strip().lower()
        copy="".join(str(cut.get("image_copy", "")).split())
        narration="".join(str(cut.get("narration", "")).split())
        if role not in ALLOWED_ROLES or not copy or not narration:
            raise ValueError(f"invalid cut {i}")
        signature=(copy,narration)
        if signature in seen:
            raise ValueError(f"cut {i} repeats semantic content")
        seen.add(signature); roles.append(role)
    if len(set(roles)) < min_unique_roles:
        raise ValueError("insufficient narrative progression")
    if any(r not in roles for r in REQUIRED_ROLES):
        raise ValueError("missing required story role")
    if roles[0] != "hook" or roles[-1] != "cta":
        raise ValueError("story must open with hook and close with cta")
    return True

def release_contract():
    return {"zero_cost":True,"genre_independent":True,"human_approval_required":True,"rights_check_required":True,"manual_post_only":True,"auto_post":False}
