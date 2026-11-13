"""Cycle1433: reusable three-beat review storyboard, NOT publication approval."""
from dataclasses import dataclass

@dataclass(frozen=True)
class Beat:
    role: str
    start: float
    end: float
    caption: str

def validate(beats, duration=15.0):
    """Fail closed on missing narrative roles, timing gaps and caption text."""
    if [b.role for b in beats] != ["problem", "demo", "verification"]:
        return False
    if not beats or abs(beats[0].start)>0.001 or abs(beats[-1].end-duration)>0.001:
        return False
    return all(b.caption.strip() and b.end>b.start and
               (i==0 or abs(beats[i-1].end-b.start)<0.001)
               for i,b in enumerate(beats))

def publication_allowed(*, japanese_narration_verified=False,
                        speech_sync_verified=False, asset_rights_approved=False,
                        employee_approved=False, media_decode_verified=False):
    return all((japanese_narration_verified, speech_sync_verified,
                asset_rights_approved, employee_approved, media_decode_verified))
