"""Fail-closed release gate shared by all TikTok genres."""
def release_gate(narration_verified: bool, captions_synced: bool, approved: bool) -> bool:
    return all((narration_verified, captions_synced, approved))
