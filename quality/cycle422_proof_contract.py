"""Genre-neutral, fail-closed provenance + numeric proof + narration release gate.
Passing render checks permits only private review, not posting or employee delivery.
No network, external assets, or third-party libraries required.
"""
from decimal import Decimal, InvalidOperation
from math import isfinite


def validate_manifest(m):
    render_errors, release_errors = [], []
    duration = m.get('duration')
    if not isinstance(duration, (int, float)) or not isfinite(duration) or not 15 <= duration <= 25:
        render_errors.append('invalid_duration')
    scenes = m.get('scenes', [])
    if not isinstance(scenes, list) or not 6 <= len(scenes) <= 10:
        render_errors.append('scene_count')
        scenes = scenes if isinstance(scenes, list) else []
    seen, cursor = set(), 0.0
    for s in scenes:
        sid = s.get('id') if isinstance(s, dict) else None
        if not sid or sid in seen:
            render_errors.append('duplicate_scene_id')
        seen.add(sid)
        try:
            a, b = float(s['start']), float(s['end'])
            if not (isfinite(a) and isfinite(b) and a < b and abs(a - cursor) <= .03):
                render_errors.append('scene_timeline_gap_or_overlap')
            cursor = b
        except (TypeError, KeyError, ValueError):
            render_errors.append('invalid_scene_timing')
        asset = s.get('asset', {}) if isinstance(s, dict) else {}
        if asset.get('origin') not in ('original', 'licensed', 'user_approved') or asset.get('rights_approved') is not True:
            render_errors.append('asset_rights_missing')
        if asset.get('contains_private_data') is not False:
            render_errors.append('private_data_not_cleared')
    if isinstance(duration, (int, float)) and scenes and abs(cursor - duration) > .03:
        render_errors.append('scene_timeline_end_mismatch')
    for claim in m.get('claims', []):
        if claim.get('kind') != 'sum' or not claim.get('source_values'):
            render_errors.append('unverified_claim')
            continue
        try:
            calculated = sum((Decimal(str(v)) for v in claim['source_values']), Decimal('0'))
            if calculated != Decimal(str(claim['display_value'])):
                render_errors.append('claim_math_mismatch')
        except (InvalidOperation, ValueError, TypeError, KeyError):
            render_errors.append('invalid_claim')
    if m.get('synthetic_demo') is True and m.get('on_screen_demo_disclosure') is not True:
        render_errors.append('synthetic_demo_undisclosed')
    voice = m.get('narration', {})
    if not (voice.get('language') == 'ja' and voice.get('verified_speech') is True
            and isinstance(voice.get('audio_sha256'), str) and len(voice['audio_sha256']) == 64):
        release_errors.append('japanese_narration_not_verified')
    if not (voice.get('measured_captions') is True and voice.get('caption_alignment_verified') is True):
        release_errors.append('measured_speech_caption_alignment_missing')
    if m.get('employee_approved') is not True:
        release_errors.append('employee_approval_missing')
    if render_errors:
        release_errors.append('render_validation_failed')
    return {'render_errors': sorted(set(render_errors)), 'release_errors': sorted(set(release_errors)),
            'review_render_allowed': not render_errors, 'preflight_passed': not release_errors,
            'publication_approved': False}  # Human quality/rights review is always separate
