"""Offline orchestration adapter. No upload, publication, or external delivery."""
import hashlib
import json
import shutil
from pathlib import Path
from src.automation_engine import Engine, validate, inspect_mp4


class RendererUnavailable(RuntimeError):
    pass


def select_plan(plans):
    """Select deterministic approved plan; trend collection and AI writing are external."""
    if not isinstance(plans, list):
        raise ValueError('plans must be a list')
    approved = [p for p in plans if isinstance(p, dict) and p.get('approved') is True and p.get('script_approved') is True and p.get('assets_approved') is True and isinstance(p.get('priority'), int) and not isinstance(p.get('priority'), bool)]
    if not approved:
        raise ValueError('no approved plan; AI planning is not connected')
    chosen = sorted(approved, key=lambda p: (-p['priority'], str(p.get('plan_id', ''))))[0]
    validate(chosen)
    return chosen


def mock_renderer(request):
    """Test-only: deliberately returns no MP4 and can never pass production QA."""
    validate(request)
    return {'status': 'mock_only', 'video_path': None, 'error': 'real_renderer_not_connected'}


def production_renderer(request):
    """PR #21 adapter is intentionally unavailable until tested and approved."""
    validate(request)
    raise RendererUnavailable('renderer_not_connected')


def safe_handoff(request, video, qa, destination, *, human_approved=False, rights_approved=False):
    """Prepare local review manifest only; never send to employees or publish."""
    validate(request)
    if not (human_approved and rights_approved and qa.get('passed') is True and qa.get('human_visual_privacy_approval') is True):
        raise PermissionError('review_or_rights_pending')
    source = Path(video).resolve()
    if not source.is_file() or source.suffix.lower() != '.mp4':
        raise ValueError('missing mp4')
    target = Path(destination).resolve()
    target.mkdir(parents=True, exist_ok=True)
    output = target / (request['run_id'] + '.mp4')
    if output.exists():
        raise FileExistsError('handoff already exists')
    shutil.copyfile(source, output)
    digest = hashlib.file_digest(output.open('rb'), 'sha256').hexdigest()
    manifest = {'run_id': request['run_id'], 'account_id': request['account_id'], 'plan_id': request['plan_id'], 'status': 'local_handoff_prepared', 'sha256': digest, 'manual_tiktok_post_only': True, 'employee_delivery': 'not_performed'}
    (target / (request['run_id'] + '.handoff.json')).write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding='utf-8')
    return manifest


def process(plans, database, renderer=None, notifier=None):
    """Fail closed; notifier receives fixed event codes only, never secrets."""
    request = select_plan(plans)
    engine = Engine(database)
    try:
        submitted = engine.submit(request)
        if submitted != 'queued':
            return {'status': 'duplicate_rejected', 'run_id': request['run_id']}
        if renderer is None or renderer is mock_renderer:
            status = engine.execute(request)
        else:
            status = engine.execute(request, renderer)
        if status in ('failed', 'qa_failed', 'renderer_not_connected') and notifier is not None:
            notifier({'run_id': request['run_id'], 'event': status})
        return {'run_id': request['run_id'], 'status': status, 'mock_success': False, 'employee_delivery': 'not_performed'}
    finally:
        engine.db.close()
