"""Review-only image-first hook, genre-configurable, on a SHA-pinned fictional MP4.

Reimplementation, not v33 original. No external service, private-media upload,
publication or posting. The image comes only from the authorized local input.
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
START, END = 0, 96  # first 3.2s; next scene remains untouched
PANEL_X, PANEL_Y, PANEL_W, PANEL_H = 47, 334, 834, 706
FONT = '/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc'
REGULAR = '/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc'
GENRES = ('ai_work','sales_business','beauty','romance','saving','career',
          'wellness','science','travel_food','product_comparison_lifestyle')
REQUIRED = {'data_classification':'fictional','contains_personal_data':False,
            'contains_confidential_media':False,'review_only':True,
            'publication_approved':False,'external_upload':False,
            'automatic_posting':False,'source_rights_reviewed':False}
# Generic copy slots: no unverifiable statistics, no real names, no trademark impersonation.
COPY = {
    'ai_work': ('まだ手作業？', '最初の一歩を変える'),
    'sales_business': ('その伝え方で届く？', 'まずは相手を理解する'),
    'beauty': ('そのケア、見直す？', '基本から確認しよう'),
    'romance': ('伝え方、変えてみる？', '相手の気持ちから考える'),
    'saving': ('毎日の支出、見えてる？', 'まずは記録から'),
    'career': ('次の一歩、決めた？', '目標を言葉にしよう'),
    'wellness': ('その習慣、続けられる？', '無理のない一歩から'),
    'science': ('その疑問、調べてみる？', '観察から始めよう'),
    'travel_food': ('次の休日、どう過ごす？', '行き先を探そう'),
    'product_comparison_lifestyle': ('選ぶ前に比べた？', '条件を整理しよう'),
}

def sha256(path: Path) -> str:
    h=hashlib.sha256()
    with Path(path).open('rb') as f:
        for chunk in iter(lambda:f.read(1<<20),b''):h.update(chunk)
    return h.hexdigest()

def validate(manifest: dict, genre: str, source: Path, output: Path) -> None:
    if genre not in GENRES or set(COPY)!=set(GENRES):
        raise ValueError('Unknown or inconsistent genre')
    if any(manifest.get(k)!=v for k,v in REQUIRED.items()):
        raise ValueError('Missing rights/privacy/review-only gate')
    if not source.is_file() or source.resolve()==output.resolve():
        raise ValueError('Missing source or unsafe output path')
    if manifest.get('source_sha256')!=sha256(source):
        raise ValueError('Source SHA256 mismatch')
    if not Path(FONT).is_file() or not Path(REGULAR).is_file():
        raise ValueError('Required offline Japanese font missing')

def probe(path: Path) -> dict:
    raw=subprocess.check_output(['ffprobe','-v','error','-show_streams','-of','json',str(path)],text=True)
    s=json.loads(raw)['streams'];v=next((x for x in s if x['codec_type']=='video'),None)
    a=next((x for x in s if x['codec_type']=='audio'),None)
    if not v or not a or v['codec_name']!='h264' or a['codec_name']!='aac':
        raise ValueError('H264/AAC required')
    if (int(v['width']),int(v['height']),v['r_frame_rate'],int(v['nb_frames']))!=(1080,1920,'30/1',691):
        raise ValueError('Wrong video format')
    if abs(float(a['duration'])-691/FPS)>.12 or int(a['sample_rate'])!=48000:
        raise ValueError('Audio missing/truncated')
    return {'width':1080,'height':1920,'fps':30,'frames':691,
            'audio_sample_rate':48000,'audio_duration':float(a['duration'])}

def pcm_md5(path: Path) -> str:
    r=subprocess.run(['ffmpeg','-v','error','-i',str(path),'-map','0:a:0',
                      '-f','md5','-acodec','pcm_s16le','-ar','48000','-ac','2','-'],
                     check=True,capture_output=True,text=True)
    return r.stdout.strip()

def smoothstep(x: float) -> float:
    t=max(0.,min(1.,x));return t*t*(3-2*t)

def make_panel(photo: np.ndarray, index: int, genre: str='ai_work') -> np.ndarray:
    """Kinetic high-contrast photo headline; no edits outside the image panel."""
    if genre not in GENRES or photo.shape!=(PANEL_H,PANEL_W,3) or not 0<=index<END:
        raise ValueError('Invalid genre, photo or frame')
    # 1.00 -> 1.065x gentle push-in; deterministic across 10 genres.
    z=1.+.065*smoothstep(index/(END-1))
    w,h=round(PANEL_W/z),round(PANEL_H/z)
    # A small lateral motion, keeping the entire crop within the source image.
    x=round((PANEL_W-w)*smoothstep(index/(END-1)))
    y=round((PANEL_H-h)*.55)
    view=cv2.resize(photo[y:y+h,x:x+w],(PANEL_W,PANEL_H),interpolation=cv2.INTER_CUBIC)
    rgb=cv2.cvtColor(view,cv2.COLOR_BGR2RGB).astype(np.float32)
    # Darken lower half behind white/yellow title for readable contrast.
    yy=np.arange(PANEL_H,dtype=np.float32)[:,None,None]
    t=np.clip((yy-200)/360,0,1)
    strength=.14+.68*(t*t*(3-2*t))
    rgb=np.uint8(np.clip(rgb*(1-strength),0,255))
    im=Image.fromarray(rgb,'RGB');d=ImageDraw.Draw(im)
    accent=(255,222,74);white=(255,255,255)
    # Tiny editorial label; text is generated as real font glyphs, never AI-drawn.
    d.rounded_rectangle((35,30,300,91),radius=25,fill=(6,37,45),outline=(97,236,221),width=2)
    d.text((56,42),'AI WORK / 01' if genre=='ai_work' else 'SHORT GUIDE',font=ImageFont.truetype(REGULAR,29),fill=(237,251,249))
    title,sub=COPY[genre]
    title_font=ImageFont.truetype(FONT,78 if len(title)<=9 else 61)
    sub_font=ImageFont.truetype(FONT,37)
    # Reveal title by opacity after 0.15s; no invisible opening seconds.
    fade=smoothstep((index-3)/9)*smoothstep((END-index-1)/7)
    layer=Image.new('RGBA',im.size,(0,0,0,0));ld=ImageDraw.Draw(layer)
    # Stroke + shadow ensure readability over variable photo backgrounds.
    a=int(255*fade)
    ld.text((47,444),title,font=title_font,fill=(*accent,a),stroke_width=5,stroke_fill=(3,15,24,a))
    sub_alpha=int(255*fade*smoothstep((index-16)/10))
    ld.text((51,554),sub,font=sub_font,fill=(*white,sub_alpha),stroke_width=3,stroke_fill=(2,14,22,sub_alpha))
    im=Image.alpha_composite(im.convert('RGBA'),layer).convert('RGB')
    return cv2.cvtColor(np.array(im),cv2.COLOR_RGB2BGR)

def make_panel_video(source: Path, path: Path, genre: str) -> None:
    cap=cv2.VideoCapture(str(source));cap.set(cv2.CAP_PROP_POS_FRAMES,12)
    ok,frame=cap.read();cap.release()
    if not ok or frame.shape[:2]!=(1920,1080):
        raise ValueError('Cannot read 1080x1920 source frame')
    photo=frame[PANEL_Y:PANEL_Y+PANEL_H,PANEL_X:PANEL_X+PANEL_W].copy()
    cmd=['ffmpeg','-v','error','-y','-f','rawvideo','-pix_fmt','bgr24',
         '-s',f'{PANEL_W}x{PANEL_H}','-r',str(FPS),'-i','pipe:0',
         '-c:v','libx264','-preset','veryfast','-crf','18','-pix_fmt','yuv420p',str(path)]
    p=subprocess.Popen(cmd,stdin=subprocess.PIPE,stderr=subprocess.PIPE)
    try:
        for i in range(END):p.stdin.write(make_panel(photo,i,genre).tobytes())
        p.stdin.close();err=p.stderr.read().decode(errors='replace')
        if p.wait(timeout=180):raise RuntimeError('Panel encode failed: '+err[-1000:])
    finally:
        if p.poll() is None:p.kill()

def render(source: Path, output: Path, manifest: dict, genre: str='ai_work') -> dict:
    source,output=Path(source),Path(output)
    validate(manifest,genre,source,output)
    before=probe(source)
    output.parent.mkdir(parents=True,exist_ok=True)
    panel=output.with_suffix('.panel.tmp.mp4')
    try:
        make_panel_video(source,panel,genre)
        # Fades affect ONLY the photo panel, not the baked narration captions.
        filt=(f'[1:v]format=yuva420p,fade=t=in:st=0:d=0.10:alpha=1,'
              f'fade=t=out:st=3.0:d=0.20:alpha=1[hero];'
              f'[0:v][hero]overlay={PANEL_X}:{PANEL_Y}:eof_action=pass:format=auto[v]')
        cmd=['ffmpeg','-v','error','-y','-filter_complex_threads','2','-i',str(source),
             '-i',str(panel),'-filter_complex',filt,'-map','[v]','-map','0:a:0',
             '-c:v','libx264','-preset','veryfast','-crf','19','-pix_fmt','yuv420p',
             '-r','30','-c:a','copy','-movflags','+faststart',str(output)]
        subprocess.run(cmd,check=True,timeout=300)
    finally:
        panel.unlink(missing_ok=True)
    after=probe(output)
    subprocess.run(['ffmpeg','-v','error','-xerror','-i',str(output),'-f','null','-'],check=True,timeout=180)
    a,b=pcm_md5(source),pcm_md5(output)
    if a!=b:raise ValueError('Decoded audio changed')
    return {'before':before,'after':after,'audio_pcm_equal':True,'audio_pcm_md5':a,
            'source_sha256':sha256(source),'output_sha256':sha256(output),
            'changed_frames':[START,END-1],'overlay_xywh':[PANEL_X,PANEL_Y,PANEL_W,PANEL_H],
            'ten_genres':len(GENRES),'independent_japanese_asr_verified':False,
            'caption_semantic_sync_verified':False,'reference_v33_directly_compared':False,
            'rights_approved':False,'phone_playback_verified':False,'publication_approved':False,
            'status':'HUMAN_REVIEW / PUBLICATION_NOT_APPROVED'}

def main():
    p=argparse.ArgumentParser();p.add_argument('--source',type=Path,required=True)
    p.add_argument('--output',type=Path,required=True);p.add_argument('--manifest',type=Path,required=True)
    p.add_argument('--genre',default='ai_work');a=p.parse_args()
    print(json.dumps(render(a.source,a.output,json.loads(a.manifest.read_text()),a.genre),ensure_ascii=False,indent=2))
if __name__=='__main__':main()
