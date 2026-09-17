"""Prepare human-reviewed posting manifests only after verified media QA."""
import json
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'output'


def build():
    verification = OUT / 'video_verification.json'
    if not verification.is_file():
        raise RuntimeError('Missing actual media verification; posting packages blocked')
    report = json.loads(verification.read_text(encoding='utf-8'))
    if not report.get('passed') or not report.get('results'):
        raise RuntimeError('Media verification failed; posting packages blocked')
    accounts = {}
    for path in (ROOT / 'config/accounts').glob('*.json'):
        account = json.loads(path.read_text(encoding='utf-8'))
        if account.get('status') == 'active':
            accounts[account['employee_id']] = account
    packages = []
    for result in report['results']:
        if not result.get('passed'):
            raise RuntimeError('Individual media QA failed')
        video = Path(result['file']).resolve()
        if not video.is_file() or OUT.resolve() not in video.parents:
            raise RuntimeError('Video missing or outside output directory')
        metadata_path = video.with_name(video.stem + '_post.json')
        if not metadata_path.is_file():
            raise RuntimeError(f'Missing posting metadata for {video.name}')
        metadata = json.loads(metadata_path.read_text(encoding='utf-8'))
        employee_id = metadata.get('employee_id')
        if employee_id not in accounts:
            raise RuntimeError(f'Unknown or inactive employee_id: {employee_id!r}')
        packages.append({
            'employee_id': employee_id,
            'employee': accounts[employee_id]['name'],
            'account': accounts[employee_id]['account'],
            'video': video.name,
            'hook': metadata.get('hook'),
            'caption': metadata.get('caption'),
            'hashtags': metadata.get('hashtags', []),
            'qa': 'passed',
            'status': 'awaiting_human_review',
            'published_at': None,
            'tiktok_post_id': None,
        })
    if not packages:
        raise RuntimeError('No verified packages')
    manifest = {'generated_at': datetime.now(timezone.utc).isoformat(), 'posting_mode': 'manual_human_approval', 'packages': packages}
    (OUT / 'posting_packages.json').write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding='utf-8')
    print(f'Prepared {len(packages)} verified packages; no TikTok posts published')


if __name__ == '__main__':
    build()
