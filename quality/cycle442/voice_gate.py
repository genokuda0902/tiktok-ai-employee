"""Genre-neutral fail-closed Japanese narration proof gate (cycle442)."""
from dataclasses import dataclass

@dataclass(frozen=True)
class NarrationEvidence:
    voice_asset: str | None
    source_engine: str | None
    text_segments: tuple[str, ...]
    timing_segments: tuple[tuple[float, float], ...]
    verified_japanese_voice: bool
    rights_approved: bool

def narration_issues(e: NarrationEvidence, duration: float) -> list[str]:
    issues=[]
    if not e.voice_asset or not e.source_engine or not e.verified_japanese_voice:
        issues.append('JAPANESE_NARRATION_MISSING_OR_UNVERIFIED')
    if not e.rights_approved:
        issues.append('VOICE_RIGHTS_UNAPPROVED')
    if not e.text_segments or len(e.text_segments)!=len(e.timing_segments):
        issues.append('VOICE_CAPTION_TIMELINE_MISSING')
    else:
        last=0.
        for (a,b),text in zip(e.timing_segments,e.text_segments):
            if not text.strip() or a<last or b<=a or b>duration+.02:
                issues.append('VOICE_CAPTION_TIMELINE_INVALID');break
            last=b
    return issues

def publication_allowed(e:NarrationEvidence, duration:float, human_approved:bool)->bool:
    return human_approved and not narration_issues(e,duration)
