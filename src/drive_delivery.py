"""Google Drive original upload adapter. No employee sharing or TikTok publishing.

The caller MUST have passed real QA and human/privacy/rights checks. The injected
Drive API object can be mocked in CI; real credentials are never stored here.
Use a private destination folder, not a shared drive-wide public link.
"""
import hashlib
import io
import re
import time


class DeliveryBlocked(PermissionError):
    pass


def upload_approved_original(service, *, job_id, account_id, folder_id, video_bytes,
                             qa, human_approved=False, rights_approved=False,
                             privacy_approved=False, retries=3, sleep=time.sleep):
    if not all((human_approved is True, rights_approved is True, privacy_approved is True,
                isinstance(qa, dict), qa.get('passed') is True, qa.get('mock') is False)):
        raise DeliveryBlocked('verified_qa_and_approvals_required')
    if not all(isinstance(v, str) and re.fullmatch(r'[A-Za-z0-9_-]{1,128}', v)
               for v in (job_id, account_id, folder_id)):
        raise ValueError('invalid identifiers')
    if not isinstance(video_bytes, bytes) or not video_bytes:
        raise ValueError('nonempty verified MP4 bytes required')
    if retries < 1 or retries > 5:
        raise ValueError('invalid retries')
    from googleapiclient.http import MediaIoBaseUpload
    digest = hashlib.sha256(video_bytes).hexdigest()
    name = f'{job_id}.mp4'
    key = f'{account_id}:{job_id}'
    # A search alone cannot guarantee exactly-once uploads under concurrent writers.
    # The PostgreSQL ledger must exclusively own the upload lease before calling this.
    query = (f"name = '{name}' and '{folder_id}' in parents and trashed = false")
    def lookup():
        response = service.files().list(q=query, fields='nextPageToken,files(id,name,md5Checksum,appProperties,parents)',
                                        page_size=100).execute()
        if response.get('nextPageToken'):
            raise DeliveryBlocked('ambiguous_paginated_drive_results')
        matches = [f for f in response.get('files', []) if f.get('appProperties', {}).get('job_key') == key]
        if len(matches) > 1:
            raise DeliveryBlocked('duplicate_drive_objects_require_reconciliation')
        if matches:
            if matches[0].get('appProperties', {}).get('sha256') != digest:
                raise DeliveryBlocked('existing_drive_object_hash_mismatch')
            return matches[0]['id']
        if response.get('files'):
            raise DeliveryBlocked('filename_collision_requires_reconciliation')
        return None
    for attempt in range(retries):
        try:
            existing = lookup()
            if existing:
                return {'file_id': existing, 'sha256': digest, 'created': False}
            media = MediaIoBaseUpload(io.BytesIO(video_bytes), mimetype='video/mp4', resumable=True)
            result = service.files().create(
                body={'name': name, 'parents': [folder_id],
                      'appProperties': {'job_key': key, 'sha256': digest}},
                media_body=media, fields='id,appProperties').execute()
            if not result.get('id'):
                raise RuntimeError('drive_upload_missing_file_id')
            return {'file_id': result['id'], 'sha256': digest, 'created': True}
        except DeliveryBlocked:
            raise
        except Exception:
            # Upload might have succeeded despite a lost response. Reconcile before retry.
            try:
                existing = lookup()
                if existing:
                    return {'file_id': existing, 'sha256': digest, 'created': False}
            except DeliveryBlocked:
                raise
            if attempt == retries - 1:
                raise
            sleep(min(2 ** attempt, 8))
    raise RuntimeError('unreachable')
