"""Ten-genre proof-first scene contract for review-only video renders."""
from dataclasses import dataclass

GENRES = ('ai_work','beauty','love_psychology','saving','sales_business','career','health','science','travel_food','product_comparison')
PROOF_MODES = ('executable_code','measured_comparison','process_walkthrough','source_check')

@dataclass(frozen=True)
class ProofScene:
    genre: str
    mode: str
    claim: str
    evidence: str
    critical_box: tuple[int, int, int, int]

def validate(scene):
    if scene.genre not in GENRES or scene.mode not in PROOF_MODES:
        raise ValueError('unsupported scene')
    if not scene.claim or not scene.evidence:
        raise ValueError('missing evidence')
    x,y,w,h=scene.critical_box
    if x<60 or y<100 or x+w>1020 or y+h>1536:
        raise ValueError('unsafe caption position')
    return True
