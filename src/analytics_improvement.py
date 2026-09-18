"""Offline, privacy-conscious analytics MVP. No TikTok publishing or network calls."""
from __future__ import annotations
import argparse
import csv
import json
from collections import defaultdict
from datetime import datetime
from pathlib import Path

FIELDS = ('account_id','video_id','video_url','published_at','genre','hook_type','views','likes','comments','shares','average_watch_seconds','completion_rate','followers_gained')

def parse(row):
    for field in ('account_id','video_id','video_url','published_at'):
        if not row.get(field):
            raise ValueError(f'missing {field}')
    datetime.fromisoformat(row['published_at'].replace('Z','+00:00'))
    result = {k: row.get(k, '') for k in FIELDS}
    for key in ('views','likes','comments','shares','followers_gained'):
        value = row.get(key, '')
        result[key] = None if value in ('', None) else int(value)
        if result[key] is not None and result[key] < 0:
            raise ValueError(f'negative {key}')
    for key in ('average_watch_seconds','completion_rate'):
        value = row.get(key, '')
        result[key] = None if value in ('', None) else float(value)
        if result[key] is not None and result[key] < 0:
            raise ValueError(f'negative {key}')
    if result['completion_rate'] is not None and result['completion_rate'] > 1:
        raise ValueError('completion_rate must be fraction 0..1')
    return result

def aggregate(rows, dimension):
    groups = defaultdict(list)
    for row in rows:
        key = row['published_at'][11:13] if dimension == 'hour' else row.get(dimension) or 'unknown'
        groups[key].append(row)
    output = []
    for key, items in sorted(groups.items()):
        measured = [r for r in items if r['views'] is not None]
        output.append({'group': key, 'videos': len(items), 'measured_videos': len(measured), 'total_views': sum(r['views'] for r in measured) if measured else None, 'mean_views': round(sum(r['views'] for r in measured)/len(measured), 2) if measured else None})
    return output

def analyze(rows):
    ids = set()
    for row in rows:
        key = (row['account_id'], row['video_id'])
        if key in ids:
            raise ValueError('duplicate account_id/video_id')
        ids.add(key)
    accounts = defaultdict(list)
    for row in rows:
        accounts[row['account_id']].append(row)
    result = {}
    for account, items in sorted(accounts.items()):
        measured = [r for r in items if r['views'] is not None]
        result[account] = {'videos': len(items), 'measured_videos': len(measured), 'by_genre': aggregate(items,'genre'), 'by_hook': aggregate(items,'hook_type'), 'by_hour': aggregate(items,'hour'), 'improvement': {'status': 'insufficient_evidence', 'reason': 'At least 10 measured videos and comparable publication-age windows are required before proposing performance-driven changes.', 'next_video_instruction': 'Test one hook variation while keeping genre, duration and measurement window consistent.'}}
    return result

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('input_csv', type=Path)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    with args.input_csv.open(encoding='utf-8-sig', newline='') as handle:
        rows = [parse(row) for row in csv.DictReader(handle)]
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(analyze(rows), ensure_ascii=False, indent=2), encoding='utf-8')

if __name__ == '__main__':
    main()
