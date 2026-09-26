"""Optional GitHub Actions -> private Drive path, with readback verification.

Requires configured Drive credentials and folder. Connector-assisted one-off uploads
are independent evidence and do not configure this unattended adapter.
"""
import hashlib
import io
import json
import os
import subprocess
from pathlib import Path

def sha(path):return hashlib.sha256(Path(path).read_bytes()).hexdigest()

def private_folder(folder,credential_kind):
    if folder.get('mimeType')!='application/vnd.google-apps.folder':raise ValueError('Not a Drive folder')
    if any(p.get('type') in ('anyone','domain') for p in folder.get('permissions',[])):raise PermissionError('Public/domain folder')
    if folder.get('capabilities',{}).get('canAddChildren') is not True:raise PermissionError('No write permission')
    if credential_kind=='service_account' and not folder.get('driveId'):raise PermissionError('Service account requires shared drive')

def persist(path,expected_sha,folder_id,credential_json):
    if not folder_id or not credential_json:raise RuntimeError('DRIVE_REVIEW_FOLDER_ID and DRIVE_REVIEW_AUTH_JSON required')
    file=Path(path).resolve(strict=True)
    if sha(file)!=expected_sha:raise ValueError('Source hash mismatch')
    info=json.loads(credential_json)
    scope=['https://www.googleapis.com/auth/drive.file']
    kind=info.get('type')
    if kind=='authorized_user':
        from google.oauth2.credentials import Credentials
        credentials=Credentials.from_authorized_user_info(info,scopes=scope)
    elif kind=='service_account':
        from google.oauth2 import service_account
        credentials=service_account.Credentials.from_service_account_info(info,scopes=scope)
    else:raise ValueError('Unsupported Drive credential type')
    from googleapiclient.discovery import build
    from googleapiclient.http import MediaFileUpload,MediaIoBaseDownload
    drive=build('drive','v3',credentials=credentials,cache_discovery=False)
    folder=drive.files().get(fileId=folder_id,fields='id,mimeType,driveId,capabilities(canAddChildren),permissions(id,type,role)',supportsAllDrives=True).execute()
    private_folder(folder,kind)
    # New immutable name. Never silently trust an existing file with the same name.
    name=file.stem+'_'+expected_sha[:12]+'.mp4'
    existing=drive.files().list(q=f"name = '{name}' and '{folder_id}' in parents and trashed = false",fields='files(id,name),nextPageToken',supportsAllDrives=True,includeItemsFromAllDrives=True).execute()
    if existing.get('files') or existing.get('nextPageToken'):raise FileExistsError('Existing or ambiguous Drive media requires manual reconciliation')
    created=drive.files().create(body={'name':name,'parents':[folder_id],'description':'UNAPPROVED REVIEW ONLY'},media_body=MediaFileUpload(str(file),mimetype='video/mp4',resumable=True),fields='id,name,permissions(id,type,role)',supportsAllDrives=True).execute()
    if any(p.get('type') in ('anyone','domain') for p in created.get('permissions',[])):raise PermissionError('Created media has broad permission')
    buf=io.BytesIO();request=drive.files().get_media(fileId=created['id'],supportsAllDrives=True)
    downloader=MediaIoBaseDownload(buf,request)
    done=False
    while not done:_,done=downloader.next_chunk()
    downloaded=buf.getvalue();actual=hashlib.sha256(downloaded).hexdigest()
    if actual!=expected_sha:raise ValueError('Drive readback hash mismatch')
    temp=file.parent/(file.stem+'.drive_readback.mp4');temp.write_bytes(downloaded)
    try:
        probe=json.loads(subprocess.check_output(['ffprobe','-v','error','-show_streams','-show_format','-of','json',str(temp)]))
        subprocess.run(['ffmpeg','-v','error','-xerror','-i',str(temp),'-f','null','-'],check=True)
        v=next(s for s in probe['streams'] if s['codec_type']=='video')
        if (v['width'],v['height'])!=(1080,1920) or not any(s['codec_type']=='audio' for s in probe['streams']):raise ValueError('Drive media invalid')
    finally:temp.unlink(missing_ok=True)
    return {'status':'DRIVE_PERSISTED_VERIFIED','file_id':created['id'],'upload_sha256':expected_sha,'download_sha256':actual,'resolution':[1080,1920],'duration_seconds':float(probe['format']['duration'])}

if __name__=='__main__':
    import sys
    result=persist(sys.argv[1],sys.argv[2],os.getenv('DRIVE_REVIEW_FOLDER_ID'),os.getenv('DRIVE_REVIEW_AUTH_JSON'))
    print(json.dumps(result))
