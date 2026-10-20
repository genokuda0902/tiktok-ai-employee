"""Cross-genre kinetic hook and visual-loop contract (review-only)."""
from dataclasses import dataclass
GENRES=('ai_productivity','career','business','finance_education','lifestyle','beauty','food','travel','learning','entertainment')
@dataclass(frozen=True)
class HookState:
    reveal:float
    arrow:float
    badge:float
def clamp01(v):return max(0.,min(1.,float(v)))
def ease(v):
    v=clamp01(v)
    return v*v*(3-2*v)
def hook_state(t):
    if not 0<=t<=3:raise ValueError('hook time outside 0..3')
    return HookState(ease(t/1.1),ease((t-.22)/.85),ease((t-.9)/.7))
def outro_progress(t):
    if not 0<=t<=3:raise ValueError('outro time outside 0..3')
    return ease((t-1.9)/1.08)
def can_publish(*,rights_approved=False,employee_approved=False,japanese_voice_verified=False,sync_verified=False,phone_playback_verified=False):
    return all((rights_approved,employee_approved,japanese_voice_verified,sync_verified,phone_playback_verified))
