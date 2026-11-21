"""Shared, fail-closed review checks for 10 content genres. No publication approval implied."""
def review(metadata):
    failures=[]
    if metadata.get("width",0)<720 or metadata.get("height",0)<1280: failures.append("resolution")
    if metadata.get("fps",0)<24: failures.append("frame_rate")
    if not metadata.get("japanese_speech_verified",False): failures.append("japanese_speech")
    if not metadata.get("captions_speech_aligned",False): failures.append("caption_alignment")
    if not metadata.get("assets_approved",False): failures.append("asset_rights")
    if not metadata.get("privacy_checked",False): failures.append("privacy")
    if not metadata.get("employee_approved",False): failures.append("employee_approval")
    return {"publication_approved":not failures,"failures":failures}
