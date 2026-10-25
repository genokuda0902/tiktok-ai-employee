"""Review-only mobile focus on actual fictional Calc footage, never publish.

Reimplementation on a locally supplied, SHA-pinned MP4. Source is not uploaded.
"""
from __future__ import annotations
import argparse
import hashlib
import json
import subprocess
from pathlib import Path
import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont

FPS = 30
START, END = 170, 249
PANEL_W, PANEL_H = 930, 470
PANEL_X, PANEL_Y = 65, 530
ZOOM = (920 / 470, 410 / 210)
CROPS = ((90, 680, 470, 210), (460, 680, 470, 210))
FONT = '/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc'
GENRES = ('ai_work','sales_business','beauty','romance','saving','career',
          'wellness','science','travel_food','product_comparison_lifestyle')
REQUIRED = {'data_classification':'fictional','contains_personal_data':False,
            'contains_confidential_media':False,'review_only':True,
            'publication_approved':False,'external_upload':False,
            'automatic_posting':False,'source_rights_reviewed':False}


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with Path(path).open('rb') as f:
        for block in iter(lambda:f.read(1024*1024),b''):
            h.update(block)
    return h.hexdigest()


def validate(manifest: dict, genre: str, source: Path, output: Path) -> None:
    if genre not in GENRES or len(GENRES)!=10:
        raise ValueError('Unsupported genre')
    if any(manifest.get(k)!=v for k,v in REQUIRED.items()):
        raise ValueError('Fail closed: rights/privacy/review status missing')
    if not source.is_file() or source.resolve()==output.resolve():
        raise ValueError('Source missing or output overwrites source')
    if manifest.get('source_sha256')!=sha256(source):
        raise ValueError('Pinned source SHA256 mismatch')


def probe(path: Path) -> dict:
    r=subprocess.check_output(['ffprobe','-v','error','-show_streams','-of','json',str(path)],text=True)
    s=json.loads(r)['streams']
    v=next((x for x in s if x['codec_type']=='video'),None)
    a=next((x for x in s if x['codec_type']=='audio'),None)
    if not v or not a or v['codec_name']!='h264' or a['codec_name']!='aac':
        raise ValueError('H264 and AAC required')
    if (int(v['width']),int(v['height']),v['r_frame_rate'],int(v['nb_frames']))!=(1080,1920,'30/1',691):
        raise ValueError('Unexpected geometry or frame count')
    if abs(float(a['duration'])-691/FPS)>.12:
        raise ValueError('Audio truncated')
    return {'width':1080,'height':1920,'fps':30,'frames':691,
            'audio_sample_rate':int(a['sample_rate']),'audio_duration':float(a['duration'])}


def audio_md5(path: Path) -> str:
    p=subprocess.run(['ffmpeg','-v','error','-i',str(path),'-map','0:a:0',
                      '-f','md5','-acodec','pcm_s16le','-ar','48000','-ac','2','-'],
                     check=True,capture_output=True,text=True)
    return p.stdout.strip()


def frame_panel(frame: np.ndarray, index: int, genre: str='ai_work') -> np.ndarray:
    """Two-beat 2x zoom into actual table; no fictional UI or metric claims."""
    if genre not in GENRES or frame.shape[:2]!=(1920,1080) or not 0<=index<END-START:
        raise ValueError('Invalid frame/genre/index')
    def crop(n: int):
        x,y,w,h=CROPS[n]
        return cv2.resize(frame[y:y+h,x:x+w],(920,410),interpolation=cv2.INTER_CUBIC)
    first,second=crop(0),crop(1)
    # Smooth 6-frame change of focus rather than an abrupt UI cut.
    blend=min(1.,max(0.,(index-36)/6))
    view=cv2.addWeighted(first,1-blend,second,blend,0)
    panel=np.full((PANEL_H,PANEL_W,3),(41,29,11),dtype=np.uint8)
    panel[53:463,5:925]=view
    cv2.rectangle(panel,(3,51),(926,466),(206,211,71),3)
    title='実際の表計算画面を拡大'
    label='入力値を確認' if index<42 else '計算結果を確認'
    pil=Image.fromarray(cv2.cvtColor(panel,cv2.COLOR_BGR2RGB))
    d=ImageDraw.Draw(pil)
    d.text((17,7),title,font=ImageFont.truetype(FONT,27),fill=(245,250,252))
    d.text((702,12),label,font=ImageFont.truetype(FONT,18),fill=(99,235,216))
    return cv2.cvtColor(np.array(pil),cv2.COLOR_RGB2BGR)


def build_panel(source: Path, panel_path: Path, genre: str):
    cap=cv2.VideoCapture(str(source))
    cap.set(cv2.CAP_PROP_POS_FRAMES,START)
    cmd=['ffmpeg','-v','error','-y','-f','rawvideo','-pix_fmt','bgr24',
         '-s',f'{PANEL_W}x{PANEL_H}','-r',str(FPS),'-i','pipe:0',
         '-c:v','libx264','-preset','veryfast','-crf','17','-pix_fmt','yuv420p',str(panel_path)]
    p=subprocess.Popen(cmd,stdin=subprocess.PIPE,stderr=subprocess.PIPE)
    try:
        for i in range(END-START):
            ok,frame=cap.read()
            if not ok:
                raise RuntimeError(f'Unable to read source frame {START+i}')
            p.stdin.write(frame_panel(frame,i,genre).tobytes())
        p.stdin.close()
        err=p.stderr.read().decode(errors='replace')
        if p.wait(timeout=120):
            raise RuntimeError('Panel encode failed: '+err[-1500:])
    finally:
        cap.release()
        if p.poll() is None:
            p.kill()


def render(source: Path, output: Path, manifest: dict, genre: str='ai_work') -> dict:
    source,output=Path(source),Path(output)
    validate(manifest,genre,source,output)
    before=probe(source)
    output.parent.mkdir(parents=True,exist_ok=True)
    panel=output.with_suffix('.focus.tmp.mp4')
    try:
        build_panel(source,panel,genre)
        duration=(END-START)/FPS
        filt=(f'[1:v]format=yuva420p,fade=t=in:st=0:d=0.18:alpha=1,'
              f'fade=t=out:st={duration-.18:.5f}:d=0.18:alpha=1,'
              f'setpts=PTS+{START/FPS:.8f}/TB[focus];'
              f'[0:v][focus]overlay={PANEL_X}:{PANEL_Y}:eof_action=pass:format=auto[v]')
        cmd=['ffmpeg','-v','error','-y','-filter_complex_threads','2',
             '-i',str(source),'-i',str(panel),'-filter_complex',filt,
             '-map','[v]','-map','0:a:0','-c:v','libx264','-preset','veryfast',
             '-crf','19','-pix_fmt','yuv420p','-r','30','-c:a','copy',
             '-movflags','+faststart',str(output)]
        subprocess.run(cmd,check=True,timeout=300)
    finally:
        panel.unlink(missing_ok=True)
    after=probe(output)
    subprocess.run(['ffmpeg','-v','error','-xerror','-i',str(output),'-f','null','-'],check=True,timeout=180)
    am,bm=audio_md5(source),audio_md5(output)
    if am!=bm:
        raise ValueError('Decoded audio changed')
    return {'before':before,'after':after,'audio_pcm_equal':True,'audio_pcm_md5':am,
            'source_sha256':sha256(source),'output_sha256':sha256(output),
            'zoom_scale_x':ZOOM[0],'zoom_scale_y':ZOOM[1],
            'changed_frames':[START,END-1],'overlay_xy':[PANEL_X,PANEL_Y],
            'ten_genres':len(GENRES),'japanese_asr_verified':False,
            'caption_semantic_sync_verified':False,'rights_approved':False,
            'publication_approved':False,'phone_playback_verified':False,
            'reference_v33_directly_compared':False,'status':'HUMAN_REVIEW / PUBLICATION_NOT_APPROVED'}


def main():
    p=argparse.ArgumentParser()
    p.add_argument('--source',type=Path,required=True)
    p.add_argument('--output',type=Path,required=True)
    p.add_argument('--manifest',type=Path,required=True)
    p.add_argument('--genre',default='ai_work')
    a=p.parse_args()
    print(json.dumps(render(a.source,a.output,json.loads(a.manifest.read_text()),a.genre),ensure_ascii=False,indent=2))

if __name__=='__main__': main()
