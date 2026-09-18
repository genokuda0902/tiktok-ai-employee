"""Stage the existing v20 rendered video for human-reviewed posting. No publishing."""
import json
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'output'
SOURCE = OUT / 'v20_motion' / 'AI時短ラボ_01_v20_final.mp4'
QUEUE = ROOT / 'content' / 'ai_jitan_lab' / 'queue.json'
ACCOUNT = ROOT / 'config' / 'accounts' / 'okuda.json'


def main():
    if not SOURCE.is_file() or SOURCE.stat().st_size == 0:
        raise RuntimeError('v20 render missing: posting package blocked')
    queue = json.loads(QUEUE.read_text(encoding='utf-8'))
    account = json.loads(ACCOUNT.read_text(encoding='utf-8'))
    if account.get('status') != 'active':
        raise RuntimeError('Account is inactive')
    # The existing v20 renderer has a fixed Excel script, not the daily queue's
    # two unrelated topics. Never attach an unrelated caption automatically.
    target = OUT / 'okuda_v20_01.mp4'
    shutil.copyfile(SOURCE, target)
    metadata = {
        'employee_id': account['employee_id'],
        'account': account['account'],
        'hook': 'Excel作業をAIで時短',
        'caption': 'Excel作業をAIで効率化する方法を紹介します。内容を確認してから投稿してください。',
        'hashtags': ['#AI時短ラボ', '#Excel', '#AI活用', '#仕事効率化'],
        'review_required': True,
        'source': str(SOURCE.relative_to(ROOT)),
        'queue_date': queue.get('date'),
    }
    target.with_name(target.stem + '_post.json').write_text(
        json.dumps(metadata, ensure_ascii=False, indent=2), encoding='utf-8'
    )
    print(f'Staged {target.name} for human review; not published')


if __name__ == '__main__':
    main()
