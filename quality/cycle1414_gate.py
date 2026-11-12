"""Fail-closed publication checks for review-only synthetic MP4s."""
def evaluate(qa, approved=False):
    problems=[]
    if qa.get("audio_streams",0)<1: problems.append("missing_audio")
    if qa.get("japanese_narration")!="VERIFIED": problems.append("unverified_japanese_narration")
    if qa.get("speech_synced_captions")!="VERIFIED": problems.append("unsynced_captions")
    if qa.get("decode")!="PASS": problems.append("decode_failed")
    if qa.get("resolution")!=[1080,1920]: problems.append("resolution_unverified")
    if not approved: problems.append("employee_approval_missing")
    return {"publication_approved":not problems,"issues":problems}
