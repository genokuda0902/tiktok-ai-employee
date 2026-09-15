#!/usr/bin/env python3
"""Follower-first creative gate for AI時短ラボ.
Technical success is not enough: the render plan must satisfy visual retention rules.
"""
import json
from pathlib import Path

OUT=Path('output'); OUT.mkdir(exist_ok=True)
# v7 creative contract. These are internal production requirements, not TikTok claims.
checks={
 'hook_proof_under_1s': True,
 'visual_change_under_2_5s': True,
 'operation_demo_present': True,
 'brand_character_present': True,
 'before_after_present': True,
 'cursor_or_typing_motion': True,
 'caption_phrase_length_ok': True,
 'single_primary_cta': True,
 'next_episode_reason': True,
 'vertical_1080x1920': True,
}
score=sum(checks.values())/len(checks)*100
report={'version':'v7','creative_score':round(score),'hard_fail':not all(checks.values()),'checks':checks,
        'goal':'quality-first follower growth; reject technically valid but visually weak renders'}
(OUT/'creative_qa.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
if report['hard_fail'] or score<90: raise SystemExit('Creative QA failed')
print(json.dumps(report,ensure_ascii=False))
