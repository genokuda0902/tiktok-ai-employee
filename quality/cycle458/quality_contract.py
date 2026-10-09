"""Genre-neutral visual evidence and publication safety contract; review-only."""
from dataclasses import dataclass

STAGES = ('HOOK','BEFORE','INPUT','TRANSFORM','PROOF','RESULT','COMPARE','CTA')
SAFE_CAPTION = (38, 1020, 682, 1120)

@dataclass(frozen=True)
class Scene:
    kind: str
    start: float
    end: float
    caption: str
    evidence: tuple = ()

def check_story(scenes, *, duration=20, manifest=None):
    if not scenes or scenes[0].start != 0 or scenes[-1].end != duration:
        raise ValueError('timeline coverage')
    if any(s.kind not in STAGES or not s.caption or s.start >= s.end for s in scenes):
        raise ValueError('invalid scene')
    if any(abs(a.end - b.start) > 1e-6 for a, b in zip(scenes, scenes[1:])):
        raise ValueError('timeline gap/overlap')
    if scenes[0].end > 2.0 or scenes[0].kind != 'HOOK':
        raise ValueError('hook must start at zero and resolve within 2s')
    kinds = [s.kind for s in scenes]
    if not all(k in kinds for k in ('BEFORE','TRANSFORM','PROOF','RESULT','COMPARE','CTA')):
        raise ValueError('missing proof story')
    for s in scenes:
        if s.kind == 'PROOF' and not s.evidence:
            raise ValueError('proof without source IDs')
        if s.kind == 'PROOF' and any(str(item) not in s.caption for item in s.evidence):
            raise ValueError('proof caption does not name source IDs')
    m = manifest or {}
    if m.get('rights') != 'SYNTHETIC_ORIGINAL' or m.get('privacy') != 'NO_REAL_PERSONAL_DATA':
        raise ValueError('asset provenance not verified')
    if m.get('publication') != 'NOT_APPROVED' or m.get('auto_post') is not False:
        raise ValueError('unsafe publishing state')
    return True

def check_caption_box(box=SAFE_CAPTION):
    x0,y0,x1,y1=box
    return 35 <= x0 < x1 <= 685 and 970 <= y0 < y1 <= 1130

def sumif_proof(rows, *, team='A', displayed=35, evidence_ids=('R1','R3','R5')):
    if len({r['id'] for r in rows}) != len(rows):
        raise ValueError('duplicate IDs')
    chosen = [r for r in rows if r['team'] == team]
    if not chosen or tuple(r['id'] for r in chosen) != tuple(evidence_ids):
        raise ValueError('source ID mismatch')
    if sum(r['value'] for r in chosen) != displayed:
        raise ValueError('displayed total differs from source')
    return True

def publishing_gate(manifest):
    if not manifest.get('japanese_narration_human_verified'):
        return 'BLOCKED_JAPANESE_NARRATION_UNVERIFIED'
    if not manifest.get('caption_voice_sync_verified'):
        return 'BLOCKED_CAPTION_VOICE_SYNC_UNVERIFIED'
    if manifest.get('human_review') != 'APPROVED':
        return 'BLOCKED_HUMAN_REVIEW'
    if manifest.get('rights') != 'SYNTHETIC_ORIGINAL':
        return 'BLOCKED_RIGHTS'
    return 'READY_FOR_EMPLOYEE_MANUAL_POST_REVIEW'
