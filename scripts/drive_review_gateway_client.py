"""Send one pinned review MP4 to the owner-executed Apps Script gateway."""
import base64
import hashlib
import hmac
import json
import os
import sys
import time
import urllib.request
from pathlib import Path

EXPECTED = 'd8b3c0736dbf29cbf528ccca19acdd7172175b73ec00e7d23a9b3b4f5933838f'
NAME = 'pi5_review_20s_REVIEW_ONLY.mp4'
MAX_BYTES = 25 * 1024 * 1024


def _canonical(timestamp, filename, digest, content_b64):
    return '\n'.join((str(timestamp), filename, digest, content_b64)).encode()


def _digest(data):
    return hashlib.sha256(data).hexdigest()


def build_payload(data, secret, timestamp=None):
    if not secret:
        raise RuntimeError('BLOCKED: Drive gateway secret missing')
    if not data or len(data) > MAX_BYTES:
        raise RuntimeError('BLOCKED: review MP4 size is not allowed')
    digest = _digest(data)
    if digest != EXPECTED or os.environ.get('EXPECTED_SHA256') != EXPECTED:
        raise RuntimeError('BLOCKED: source MP4 SHA-256 mismatch')
    timestamp = int(time.time() if timestamp is None else timestamp)
    content_b64 = base64.b64encode(data).decode('ascii')
    signature = hmac.new(
        secret.encode(),
        _canonical(timestamp, NAME, digest, content_b64),
        hashlib.sha256,
    ).hexdigest()
    return {
        'version': 1,
        'timestamp': timestamp,
        'filename': NAME,
        'sha256': digest,
        'content_b64': content_b64,
        'signature': signature,
    }


def send(path, url, secret):
    if not url.startswith('https://script.google.com/macros/s/'):
        raise RuntimeError('BLOCKED: invalid Apps Script gateway URL')
    payload = build_payload(Path(path).read_bytes(), secret)
    request = urllib.request.Request(
        url,
        data=json.dumps(payload, separators=(',', ':')).encode(),
        headers={'Content-Type': 'application/json'},
        method='POST',
    )
    try:
        with urllib.request.urlopen(request, timeout=120) as response:
            result = json.loads(response.read().decode())
    except Exception:
        raise RuntimeError('BLOCKED: Drive gateway request failed') from None
    if not result.get('ok'):
        code = result.get('error', 'unknown')
        raise RuntimeError(f'BLOCKED: Drive gateway rejected request; reason={code}')
    if (result.get('readback_sha256') != EXPECTED or
            result.get('readback_sha256_match') is not True or
            result.get('posting') is not False):
        raise RuntimeError('BLOCKED: Drive gateway readback verification failed')
    print('DRIVE_GATEWAY_FILE_ID=' + str(result.get('file_id', '')), flush=True)
    print('DRIVE_READBACK_SHA256=' + result['readback_sha256'], flush=True)
    print('DRIVE_READBACK_SHA256_MATCH=true; QUALITY=UNAPPROVED_REVIEW_ONLY; POSTING=false', flush=True)


def main(path):
    url = os.environ.get('DRIVE_REVIEW_WEBAPP_URL', '')
    secret = os.environ.get('DRIVE_REVIEW_WEBHOOK_SECRET', '')
    if not url or not secret:
        raise RuntimeError('BLOCKED: Drive gateway URL/secret missing')
    send(path, url, secret)


if __name__ == '__main__':
    if len(sys.argv) != 2:
        raise SystemExit('Usage: drive_review_gateway_client.py /path/to/pi5_review_20s.mp4')
    main(sys.argv[1])
