"""Cycle 257 hook/body/close contract. No publication action."""
def validate_cycle257(plan):
    errors=[]
    if plan.get("structure") != ["HOOK","BODY","CLOSE"]:
        errors.append("structure must be HOOK/BODY/CLOSE")
    if plan.get("hook_end_seconds",99) > 2.0:
        errors.append("hook must finish by 2s")
    if plan.get("publication_gate") != "HUMAN_REVIEW / PUBLICATION_NOT_APPROVED":
        errors.append("publication gate must fail closed")
    if plan.get("auto_post") is not False:
        errors.append("auto_post must remain false")
    return errors
