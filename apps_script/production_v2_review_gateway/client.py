"""Pinned, fail-closed client for the unapproved Japanese review artifact.

The caller must download artifact 10912987040 independently and verify its ZIP
contents before invoking this client. No old Pi5 artifact is accepted.
"""
import base64
import hashlib
import hmac
import json
import os
import sys
import time
import urllib.request
from pathlib import Path

EXPECTED_SHA256 = '9e1cbf5fb018efa14571c39f4631d984d92fdd86b477d95bf24d17a1c81d1939'
EXPECTED_NAME = 'video_jp_review_0001_v1_REVIEW_ONLY.mp4'
MAX_BYTES = 25 * 1024 * 1024


def build_payload(data: bytes, secret: str, timestamp: int | None = None) -> dict:
    if not secret:
        raise ValueError('gateway secret missing')
    if not data or len(data) > MAX_BYTES:
        raise ValueError('review MP4 size not allowed')
    digest = hashlib.sha256(data).hexdigest()
    if digest != EXPECTED_SHA256:
        raise ValueError('source artifact SHA-256 mismatch')
    timestamp = int(time.time()) if timestamp is None else timestamp
    content = base64.b64encode(data).decode('ascii')
    canonical = '\n'.join((str(timestamp), EXPECTED_NAME, digest, content))
    signature = hmac.new(secret.encode(), canonical.encode(), hashlib.sha256).hexdigest()
    return dict(version=1, timestamp=timestamp, filename=EXPECTED_NAME,
                sha256=digest, content_b64=content, signature=signature)


def send(path: Path, url: str, secret: str) -> dict:
    if not url.startswith('https://script.google.com/macros/s/') or not url.endswith('/exec'):
        raise ValueError('invalid Apps Script deployment URL')
    payload = build_payload(path.read_bytes(), secret)
    request = urllib.request.Request(url,
        data=json.dumps(payload, separators=(',', ':')).encode(),
        headers={'Content-Type': 'application/json'}, method='POST')
    try:
        with urllib.request.urlopen(request, timeout=120) as response:
            result = json.loads(response.read().decode())
    except Exception as error:
        raise RuntimeError(f'gateway request failed: {type(error).__name__}') from None
    if result.get('ok') is not True:
        raise RuntimeError('gateway rejected request: ' + str(result.get('error', 'unknown')))
    if result.get('readback_sha256') != EXPECTED_SHA256 or \
            result.get('readback_sha256_match') is not True or \
            result.get('posting') is not False or \
            result.get('quality') != 'QUALITY_NOT_APPROVED' or \
            not result.get('file_id'):
        raise RuntimeError('gateway readback verification failed')
    return {'file_id': result['file_id'], 'upload_sha256': EXPECTED_SHA256,
            'readback_sha256': result['readback_sha256'],
            'status': 'GATEWAY_OWNER_READBACK_MATCH_UNAPPROVED'}


if __name__ == '__main__':
    if len(sys.argv) != 2:
        raise SystemExit('Usage: python client.py path/to/video.mp4')
    result = send(Path(sys.argv[1]), os.environ.get('DRIVE_REVIEW_WEBAPP_URL', ''),
                  os.environ.get('DRIVE_REVIEW_WEBHOOK_SECRET', ''))
    print(json.dumps(result, sort_keys=True))
