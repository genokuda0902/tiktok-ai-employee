"""Isolated REVIEW ONLY delivery. No publishing, approvals or PR merge."""
import hashlib
import io
import json
import os
import sys
from pathlib import Path

EXPECTED = 'd8b3c0736dbf29cbf528ccca19acdd7172175b73ec00e7d23a9b3b4f5933838f'
FOLDER = '14rtOvwFKmycVO5Irq1X8QJ4-vgO2xUMk'
NAME = 'pi5_review_20s_REVIEW_ONLY.mp4'


def _credential_kind(info):
    kind = info.get('type') if isinstance(info, dict) else None
    if kind not in ('service_account', 'authorized_user'):
        raise RuntimeError(
            'BLOCKED: Drive credential JSON must be service_account or authorized_user')
    return kind


def _build_credentials(info):
    """Build least-scope credentials without logging credential contents."""
    scope = ['https://www.googleapis.com/auth/drive.file']
    kind = _credential_kind(info)
    if kind == 'service_account':
        from google.oauth2 import service_account
        return kind, service_account.Credentials.from_service_account_info(
            info, scopes=scope)
    from google.oauth2.credentials import Credentials
    return kind, Credentials.from_authorized_user_info(info, scopes=scope)


def _drive_error_reason(exc):
    """Return only the Drive API reason code; never expose credential material."""
    content = getattr(exc, 'content', b'')
    try:
        payload = json.loads(content.decode() if isinstance(content, bytes) else content)
        errors = payload.get('error', {}).get('errors', [])
        return errors[0].get('reason') if errors else None
    except Exception:
        return None


def _validate_destination(folder, credential_kind):
    if folder.get('mimeType') != 'application/vnd.google-apps.folder':
        raise RuntimeError('BLOCKED: destination is not a Drive folder')
    if any(p.get('type') in ('anyone', 'domain')
           for p in folder.get('permissions', [])):
        raise RuntimeError('BLOCKED: public/domain folder permission detected')
    if folder.get('capabilities', {}).get('canAddChildren') is not True:
        raise RuntimeError('BLOCKED: selected Drive identity cannot add files to destination')
    # Service accounts have no personal Drive storage quota. They can upload only
    # where a Workspace shared drive owns the resulting file.
    if credential_kind == 'service_account' and not folder.get('driveId'):
        raise RuntimeError(
            'BLOCKED: service account cannot store files in My Drive; use '
            'authorized_user OAuth or a Workspace shared drive')


def main(path):
    from googleapiclient.discovery import build
    from googleapiclient.http import MediaFileUpload, MediaIoBaseDownload

    raw = (os.environ.get('DRIVE_AUTH_JSON', '') or
           os.environ.get('DRIVE_SERVICE_ACCOUNT_JSON', ''))
    if not raw:
        raise RuntimeError('BLOCKED: DRIVE_REVIEW_AUTH_JSON credential missing')
    # Never log secret material or credential exceptions that may contain private data.
    try:
        info = json.loads(raw)
        credential_kind, credentials = _build_credentials(info)
    except Exception:
        raise RuntimeError(
            'BLOCKED: invalid Drive credential JSON; check secret configuration') from None
    print('DRIVE_AUTH_KIND=' + credential_kind, flush=True)
    service = build('drive', 'v3', credentials=credentials, cache_discovery=False)
    data = Path(path).read_bytes()
    digest = hashlib.sha256(data).hexdigest()
    if digest != EXPECTED or os.environ.get('EXPECTED_SHA256') != EXPECTED:
        raise RuntimeError('BLOCKED: source MP4 SHA-256 mismatch')
    print('SOURCE_SHA256=' + digest, flush=True)
    try:
        folder = service.files().get(
            fileId=FOLDER,
            fields=('id,mimeType,driveId,capabilities(canAddChildren),'
                    'permissions(id,type,role)'),
            supportsAllDrives=True).execute()
    except Exception as exc:
        reason = _drive_error_reason(exc) or 'unknown'
        raise RuntimeError(
            'BLOCKED: cannot read destination folder; grant the selected Drive '
            f'identity access; reason={reason}') from None
    _validate_destination(folder, credential_kind)
    # Idempotent lookup: never overwrite or silently accept an existing file.
    try:
        existing = service.files().list(
            q=f"name = '{NAME}' and '{FOLDER}' in parents and trashed = false",
            fields='files(id,name),nextPageToken', pageSize=100,
            supportsAllDrives=True, includeItemsFromAllDrives=True).execute()
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
            created = service.files().create(
                body={'name': NAME, 'parents': [FOLDER],
                      'description': 'UNAPPROVED REVIEW ONLY; NOT FOR POSTING'},
                media_body=media, fields='id,name,parents,mimeType,driveId',
                supportsAllDrives=True).execute()
            file_id = created['id']
        except Exception as exc:
            reason = _drive_error_reason(exc)
            if reason == 'storageQuotaExceeded':
                raise RuntimeError(
                    'BLOCKED: Drive storageQuotaExceeded; use authorized_user OAuth '
                    'for My Drive or a Workspace shared drive') from None
            raise RuntimeError(
                'BLOCKED: Drive upload failed; verify writer access, Drive API and storage policy') from None
        print('DRIVE_CREATED_FILE_ID=' + file_id, flush=True)
    try:
        metadata = service.files().get(
            fileId=file_id, fields='id,name,parents,mimeType,driveId',
            supportsAllDrives=True).execute()
        if FOLDER not in metadata.get('parents', []) or metadata.get('mimeType') != 'video/mp4':
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
