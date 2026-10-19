ALLOWED = {"self_generated", "licensed", "public_domain"}

def check_assets(items):
    if not items:
        raise ValueError("Missing source")
    for item in items:
        if item.get("license") not in ALLOWED:
            raise ValueError("Source not cleared")
        if item.get("approved") is not True:
            raise ValueError("Review pending")
    return True
