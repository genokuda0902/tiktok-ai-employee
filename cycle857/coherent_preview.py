"""cycle857: use one fictional spreadsheet example consistently across shots.

The preview is taken from an existing private, review-only video, not a web asset.
Only video pixels within an inset are replaced. No external uploads or posting.
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

GENRES = ('ai_work','sales_business','beauty','romance','saving','career',
          'wellness','science','travel_food','product_comparison_lifestyle')
PALETTES = {g:(36+(i*11)%70,172+(i*5)%62,208-(i*7)%58) for i,g in enumerate(GENRES)}
POLICY = {'review_only':True,'publication_approved':False,'automatic_posting':False,
          'external_upload':False,'source_rights_reviewed':False,
          'contains_personal_data':False,'fictional_workflow_example':True}
WINDOW=(170,251)  # 5.667-8.367 seconds at 30 fps, 81 frames
PREVIEW_INDEX=362  # real Calc screen shown later in the same source video
PREVIEW_CROP=(90,575,860,1089)  # task table only; excludes LibreOffice toolbars/banners
COVER=(44,330,1036,1220)  # original upper title and lower captions remain untouched
FONT='/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc'
LABELS=('見本の表を先に見る','数字の並びを確認','合計まで確認する')

def sha256(path):
    h=hashlib.sha256()
    with open(path,'rb') as f:
        for b in iter(lambda:f.read(1<<20),b''):h.update(b)
    return h.hexdigest()

def streams(path):
    obj=json.loads(subprocess.check_output(['ffprobe','-v','error','-show_streams','-of','json',str(path)],text=True))
    return next((x for x in obj['streams'] if x['codec_type']=='video'),None),next((x for x in obj['streams'] if x['codec_type']=='audio'),None)

def validate(source,output,manifest,genre,window,preview_index,preview_crop):
    source,output=Path(source),Path(output)
    if genre not in GENRES or len(GENRES)!=10:raise ValueError('unknown genre')
    if not source.is_file():raise FileNotFoundError('private source missing')
    if manifest!={**POLICY,'source_sha256':sha256(source)}:raise ValueError('policy/source SHA mismatch')
    if source.resolve()==output.resolve() or output.exists():raise ValueError('refuse overwrite')
    v,a=streams(source)
    if not v or not a or (v['codec_name'],v['width'],v['height'],v['r_frame_rate'],a['codec_name'])!=('h264',1080,1920,'30/1','aac'):
        raise ValueError('requires H264 1080x1920 30fps + AAC')
    n=int(v['nb_frames'])
    if len(window)!=2 or not all(type(x)==int for x in window) or not 0<=window[0]<window[1]<=n or window[1]-window[0]<30:
        raise ValueError('invalid window')
    if type(preview_index)!=int or not 0<=preview_index<n or window[0]<=preview_index<window[1]:
        raise ValueError('preview must come from different scene')
    if len(preview_crop)!=4 or not all(type(x)==int for x in preview_crop):raise ValueError('crop coordinates')
    x0,y0,x1,y1=preview_crop
    if not 0<=x0<x1<=1080 or not 0<=y0<y1<=1920 or (x1-x0)<300 or (y1-y0)<200:
        raise ValueError('crop too small/outside frame')
    if not Path(FONT).is_file():raise FileNotFoundError('Noto Japanese font unavailable')
    return n

def preview_crop_from_frame(frame,roi):
    if frame.shape!=(1920,1080,3):raise ValueError('frame dimensions')
    x0,y0,x1,y1=roi
    return cv2.cvtColor(frame[y0:y1,x0:x1],cv2.COLOR_BGR2RGB)

def draw_panel(preview_rgb,genre,beat):
    if genre not in GENRES or beat not in (0,1,2):raise ValueError('invalid genre/beat')
    if preview_rgb.ndim!=3 or preview_rgb.shape[2]!=3:raise ValueError('RGB image required')
    W,H=COVER[2]-COVER[0],COVER[3]-COVER[1]
    color=PALETTES[genre]
    im=Image.new('RGB',(W,H),(7,22,34));d=ImageDraw.Draw(im)
    d.rounded_rectangle((10,8,W-10,H-8),radius=34,fill=(9,29,44),outline=color,width=3)
    font=lambda n:ImageFont.truetype(FONT,n)
    d.rounded_rectangle((36,34,398,93),radius=20,fill=color)
    d.text((217,64),'WORKFLOW / PREVIEW',font=font(25),anchor='mm',fill=(7,25,35))
    d.text((38,117),'完成見本は、先に決める。',font=font(47),fill=(246,249,253))
    d.text((40,185),'同じ架空データを後半の確認シーンでも使用',font=font(27),fill=(177,211,223))
    # Single consistent Calc table, cropped from scene 05. No OS banners or toolbar.
    area=(53,260,939,770)
    resized=Image.fromarray(preview_rgb).resize((area[2]-area[0],area[3]-area[1]),Image.Resampling.LANCZOS)
    im.paste(resized,area[:2]);d=ImageDraw.Draw(im)
    d.rounded_rectangle((area[0]-3,area[1]-3,area[2]+3,area[3]+3),radius=5,outline=color,width=5)
    # Highlight actual rows from the cropped spreadsheet, no generated results.
    # Pixel positions scale with the crop. The 3 beats are row, row, total.
    rel=[(0.21,0.40),(0.42,0.61),(0.82,0.98)][beat]
    y0=int(area[1]+(area[3]-area[1])*rel[0]);y1=int(area[1]+(area[3]-area[1])*rel[1])
    d.rectangle((area[0]+8,y0,area[2]-8,y1),outline=(255,205,84),width=6)
    d.rounded_rectangle((38,796,W-38,866),radius=22,fill=(14,70,83),outline=color,width=2)
    d.text((W//2,831),f'{beat+1:02d} / 03   {LABELS[beat]}',font=font(34),anchor='mm',fill=(248,250,253))
    return np.asarray(im)

def render(source,output,manifest,genre='ai_work',window=WINDOW,preview_index=PREVIEW_INDEX,preview_crop=PREVIEW_CROP):
    """Render with FFmpeg native overlay (no 4GB Python raw-frame pipe)."""
    import tempfile
    n=validate(source,output,manifest,genre,window,preview_index,preview_crop)
    cap=cv2.VideoCapture(str(source))
    cap.set(cv2.CAP_PROP_POS_FRAMES,preview_index)
    ok,ref=cap.read();cap.release()
    if not ok:raise RuntimeError('preview frame not readable')
    preview=preview_crop_from_frame(ref,preview_crop)
    frames=window[1]-window[0]
    counts=[(frames*(i+1))//3-(frames*i)//3 for i in range(3)]
    with tempfile.TemporaryDirectory(prefix='cycle857_') as td:
        files=[]
        for i in range(3):
            p=Path(td)/f'beat{i}.png'
            Image.fromarray(draw_panel(preview,genre,i)).save(p)
            files.append(p)
        # Each still lasts exactly its allocated frame count at 30fps.
        cmd=['ffmpeg','-hide_banner','-loglevel','error','-y','-i',str(source)]
        for f,count in zip(files,counts):
            cmd+=['-loop','1','-framerate','30','-t',str(count/30),'-i',str(f)]
        filt=(
            '[1:v][2:v][3:v]concat=n=3:v=1:a=0,format=yuv420p,'
            f'trim=end_frame={frames},setpts=PTS-STARTPTS+{window[0]}/30/TB[ov];'
            '[0:v][ov]overlay=x=44:y=330:shortest=0:repeatlast=0:eof_action=pass:format=auto[v]'
        )
        cmd+=['-filter_complex',filt,'-map','[v]','-map','0:a:0',
              '-c:v','libx264','-preset','ultrafast','-crf','20','-pix_fmt','yuv420p',
              '-r','30','-frames:v',str(n),'-c:a','copy','-movflags','+faststart',str(output)]
        try:subprocess.run(cmd,check=True,stdout=subprocess.DEVNULL,stderr=subprocess.PIPE)
        except subprocess.CalledProcessError as e:
            Path(output).unlink(missing_ok=True)
            raise RuntimeError('FFmpeg overlay failed: '+e.stderr.decode(errors='replace')[-1800:])
    subprocess.run(['ffmpeg','-v','error','-xerror','-i',str(output),'-f','null','-'],check=True,stdout=subprocess.DEVNULL)
    v,a=streams(output)
    if int(v['nb_frames'])!=n or a['codec_name']!='aac':raise RuntimeError('bad output stream')
    return {'cycle':857,'genre':genre,'source_sha256':sha256(source),'output_sha256':sha256(output),
            'frames':n,'changed_frames':frames,'window':list(window),'preview_frame':preview_index,
            'preview_crop':list(preview_crop),'visual_improvement':'same fictional Calc table reused from scene05 in scene03; removes toolbar/banner clutter',
            'full_av_decode':True,'independent_japanese_transcript_verified':False,
            'semantic_subtitle_sync_verified':False,'source_rights_reviewed':False,
            'smartphone_playback_verified':False,'publication_approved':False,
            'status':'HUMAN_REVIEW / PUBLICATION_NOT_APPROVED'}

if __name__=='__main__':
    ap=argparse.ArgumentParser()
    for x in ('source','output','manifest','report'):ap.add_argument('--'+x,required=True)
    ap.add_argument('--genre',default='ai_work')
    ap.add_argument('--window',nargs=2,type=int,default=list(WINDOW))
    ap.add_argument('--preview-index',type=int,default=PREVIEW_INDEX)
    args=ap.parse_args()
    m=json.loads(Path(args.manifest).read_text(encoding='utf-8'))
    report=render(args.source,args.output,m,args.genre,tuple(args.window),args.preview_index)
    Path(args.report).write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
    print(json.dumps(report,ensure_ascii=False))