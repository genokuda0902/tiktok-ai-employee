"""Isolated REVIEW ONLY delivery. No publishing, approvals or PR merge."""
import hashlib
import io
import json
import os
import sys
from pathlib import Path

EXPECTED = 'c5b0bc27be175b9c990cb4ef91d63ef2c35d045ed890c95cb6c02d329c0ae472'
FOLDER = '14rtOvwFKmycVO5Irq1X8QJ4-vgO2xUMk'
NAME = 'pi5_review_20s_REVIEW_ONLY.mp4'


def main(path):
    from google.oauth2 import service_account
    from googleapiclient.discovery import build
    from googleapiclient.http import MediaFileUpload, MediaIoBaseDownload

    raw = os.environ.get('DRIVE_SERVICE_ACCOUNT_JSON', '')
    if not raw:
        raise RuntimeError('BLOCKED: DRIVE_REVIEW_SERVICE_ACCOUNT_JSON missing')
    # Never log secret material or credential exceptions that may contain private data.
    try:
        info = json.loads(raw)
        credentials = service_account.Credentials.from_service_account_info(
            info, scopes=['https://www.googleapis.com/auth/drive.file'])
    except Exception:
        raise RuntimeError('BLOCKED: invalid Drive service account JSON; check secret configuration') from None
    service = build('drive', 'v3', credentials=credentials, cache_discovery=False)
    data = Path(path).read_bytes()
    digest = hashlib.sha256(data).hexdigest()
    if digest != EXPECTED or os.environ.get('EXPECTED_SHA256') != EXPECTED:
        raise RuntimeError('BLOCKED: source MP4 SHA-256 mismatch')
    print('SOURCE_SHA256=' + digest, flush=True)
    try:
        folder = service.files().get(fileId=FOLDER, fields='id,mimeType,shared,permissions(id,type,role)', supportsAllDrives=True).execute()
    except Exception:
        raise RuntimeError('BLOCKED: cannot read destination folder; grant service account access and Drive API scope') from None
    if folder.get('mimeType') != 'application/vnd.google-apps.folder' or folder.get('shared') is True:
        raise RuntimeError('BLOCKED: destination is not an unshared folder')
    if any(p.get('type') in ('anyone', 'domain') for p in folder.get('permissions', [])):
        raise RuntimeError('BLOCKED: public/domain folder permission detected')
    # Idempotent lookup: never overwrite or silently accept an existing file.
    try:
        existing = service.files().list(q=f"name = '{NAME}' and '{FOLDER}' in parents and trashed = false", fields='files(id,name),nextPageToken', pageSize=100).execute()
    except Exception:
        raise RuntimeError('BLOCKED: cannot list private folder; grant service account folder access') from None
    if existing.get('nextPageToken') or len(existing.get('files', [])) > 1:
        raise RuntimeError('BLOCKED: ambiguous existing Drive files; manual reconciliation required')
    if existing.get('files'):
        file_id = existing['files'][0]['id']
        print('DRIVE_EXISTING_FILE_ID=' + file_id, flush=True)
    else:
        try:
            media = MediaFileUpload(path, mimetype='video/mp4', resumable=True)
            created = service.files().create(body={'name': NAME, 'parents': [FOLDER], 'description': 'UNAPPROVED REVIEW ONLY; NOT FOR POSTING'}, media_body=media, fields='id,name,parents,mimeType,shared', supportsAllDrives=True).execute()
            file_id = created['id']
        except Exception:
            raise RuntimeError('BLOCKED: Drive upload failed; verify service account writer access, Drive API and storage policy') from None
        print('DRIVE_CREATED_FILE_ID=' + file_id, flush=True)
    try:
        metadata = service.files().get(fileId=file_id, fields='id,name,parents,mimeType,shared', supportsAllDrives=True).execute()
        if FOLDER not in metadata.get('parents', []) or metadata.get('mimeType') != 'video/mp4' or metadata.get('shared') is True:
            raise RuntimeError('BLOCKED: uploaded file metadata/private location verification failed')
        request = service.files().get_media(fileId=file_id, supportsAllDrives=True)
        sink = io.BytesIO()
        downloader = MediaIoBaseDownload(sink, request)
        done = False
        while not done:
            _, done = downloader.next_chunk()
        actual = hashlib.sha256(sink.getvalue()).hexdigest()
    except RuntimeError:
        raise
    except Exception:
        raise RuntimeError('BLOCKED: Drive authenticated readback failed; verify service account reader access') from None
    print('DRIVE_FILE_ID=' + file_id, flush=True)
    print('DRIVE_READBACK_SHA256=' + actual, flush=True)
    if actual != EXPECTED:
        raise RuntimeError('BLOCKED: Drive readback SHA-256 mismatch')
    print('DRIVE_READBACK_SHA256_MATCH=true; QUALITY=UNAPPROVED_REVIEW_ONLY; POSTING=false', flush=True)


if __name__ == '__main__':
    if len(sys.argv) != 2:
        raise SystemExit('Usage: drive_review_artifact_handoff.py /path/to/pi5_review_20s.mp4')
    main(sys.argv[1])
