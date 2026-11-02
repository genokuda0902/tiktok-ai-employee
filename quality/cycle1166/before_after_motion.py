#!/usr/bin/env python3
"""10-genre, review-only procedural BEFORE/AFTER proof montage.

Private input media never leaves the local machine. This is not v33 recovery,
Japanese ASR, evidence of actual time saved, or publication authorization.
"""
import argparse
import hashlib
import json
from pathlib import Path
import subprocess
import tempfile
from PIL import Image, ImageDraw, ImageFont

POLICY = 'HUMAN_REVIEW/PUBLICATION_NOT_APPROVED'
PALETTES = {
    'ai': ('#30D5CE','#6DA6FF'), 'business': ('#E5B769','#71B2ED'),
    'money': ('#54C78C','#74A7E7'), 'learning': ('#AC9AFF','#6ECAD6'),
    'health': ('#72D6C3','#91B7FF'), 'food': ('#F3B679','#6BC8B4'),
    'travel': ('#79C8ED','#F3BD83'), 'beauty': ('#E4A8D4','#B2B6EF'),
    'career': ('#F4C277','#8ABBE9'), 'life': ('#8FD3A9','#B8B2F1')
}
START, END = 20.50, 22.99
CANVAS = (1080,1920)
FONT_REG = '/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc'
FONT_BOLD = '/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc'


def cmd(argv, capture=False):
    return subprocess.run(argv, check=True, stdout=subprocess.PIPE if capture else subprocess.DEVNULL,
                          stderr=subprocess.PIPE if capture else subprocess.DEVNULL)


def digest(path):
    h=hashlib.sha256()
    with open(path,'rb') as f:
        for b in iter(lambda:f.read(1<<20),b''): h.update(b)
    return h.hexdigest()


def meta(path):
    j=json.loads(cmd(['ffprobe','-v','error','-show_streams','-show_format','-of','json',str(path)],True).stdout)
    v=next(s for s in j['streams'] if s['codec_type']=='video')
    a=next(s for s in j['streams'] if s['codec_type']=='audio')
    return dict(codec=v['codec_name'],width=int(v['width']),height=int(v['height']),fps=v['avg_frame_rate'],
                frames=int(v.get('nb_frames') or 0),duration=float(j['format']['duration']),
                audio=a['codec_name'],rate=int(a['sample_rate']),size=Path(path).stat().st_size)


def audio_digest(path):
    raw=cmd(['ffmpeg','-v','error','-i',str(path),'-map','0:a:0','-c:a','copy','-f','adts','pipe:1'],True).stdout
    return hashlib.sha256(raw).hexdigest()


def validate(manifest, source):
    if not isinstance(manifest,dict) or manifest.get('policy')!=POLICY or manifest.get('asset_approval')!='review_only_no_publication' or manifest.get('manual_post_only') is not True:
        raise ValueError('Fail closed: review-only approval and manual-post policy required')
    if manifest.get('genre') not in PALETTES or manifest.get('source_sha256')!=digest(source):
        raise ValueError('Fail closed: genre/source hash')
    if manifest.get('window') != [START,END]:
        raise ValueError('Fail closed: fixed scene-8 window required')
    m=meta(source)
    if (m['codec'],m['width'],m['height'],m['fps'],m['audio'],m['rate']) != ('h264',1080,1920,'30/1','aac',48000):
        raise ValueError('Fail closed: unexpected source media')
    if m['duration'] < END or m['duration']>23.1:
        raise ValueError('Fail closed: unsupported chapter structure')
    return m


def font(size,bold=False):
    return ImageFont.truetype(FONT_BOLD if bold else FONT_REG,size)


def panel_assets(folder,genre):
    """Entirely procedural images. The comparison is an illustrative workflow, not a speed claim."""
    accent,accent2=PALETTES[genre]
    bg=Image.new('RGBA',(920,580),(5,15,35,255)); d=ImageDraw.Draw(bg)
    d.rounded_rectangle((2,2,918,578),radius=24,outline='#497C9A',width=3)
    d.text((32,17),'WORKFLOW / BEFORE  →  AFTER',font=font(25,True),fill='#C8E8F4')
    d.text((32,520),'※架空の集計例｜公開・投稿は未承認',font=font(22),fill='#9DC0CE')
    bg.save(folder/'background.png')
    for side in ('before','after'):
        im=Image.new('RGBA',(414,412),(0,0,0,0)); p=ImageDraw.Draw(im)
        p.rounded_rectangle((2,2,410,410),radius=22,fill='#101E37' if side=='before' else '#0A2A39',outline='#52778B' if side=='before' else accent,width=3)
        p.rounded_rectangle((18,17,396,84),radius=12,fill='#233047' if side=='before' else '#174D59')
        p.text((33,25),'BEFORE' if side=='before' else 'AFTER',font=font(38,True),fill='#D8E3F1' if side=='before' else accent)
        p.text((32,95),'手作業' if side=='before' else 'AIで下書き',font=font(34,True),fill='#FFFFFF')
        if side=='before':
            for i,(dx,dy) in enumerate(((83,162),(118,178),(150,194))):
                p.rounded_rectangle((dx,dy,dx+155,dy+115),radius=6,fill='#DDE9EF',outline='#91B0C5',width=3)
                for j in range(3):p.line((dx+18,dy+25+j*22,dx+126,dy+25+j*22),fill='#7C9FB5',width=4)
            p.text((40,330),'集計 → 転記 → 確認',font=font(25,True),fill='#F6D9B4')
        else:
            p.rounded_rectangle((35,161,377,312),radius=14,fill='#EAF5F7')
            p.text((52,173),'営業A   営業B   合計',font=font(25,True),fill='#255065')
            p.line((48,223,365,223),fill='#A3C4D0',width=3)
            p.text((52,240),'46  +  29  =  75',font=font(33,True),fill='#075F67')
            p.ellipse((337,263,369,295),fill=accent)
            p.line((344,277,350,284,362,270),fill='#0B3543',width=4,joint='curve')
            p.text((34,333),'最後は人が検証',font=font(27,True),fill='#C7FFF3')
        im.save(folder/f'{side}.png')
    return [folder/x for x in ('background.png','before.png','after.png')]


def positions(t):
    """Testable slide-in timing, never draws over subtitle area y>=1280."""
    left=-430+(t-20.55)*1446 if 20.55<=t<20.90 else 76
    right=1080-(t-20.85)*1572 if 20.85<=t<21.20 else 522
    return left,right


def render(source,output,manifest,report):
    source,output,manifest,report=map(Path,(source,output,manifest,report))
    if source.resolve()==output.resolve(): raise ValueError('Cannot overwrite source')
    m=json.loads(manifest.read_text(encoding='utf-8'))
    before=validate(m,source)
    output.parent.mkdir(parents=True,exist_ok=True)
    with tempfile.TemporaryDirectory(prefix='cycle1166_') as td:
        files=panel_assets(Path(td),m['genre'])
        # Main chapter title, 3 CTA cards, narration/subtitles are untouched by the
        # compositing geometry (overlays occupy y=290..780, below heading).
        bg=f"[0:v][1:v]overlay=x=57:y=290:enable='between(t,{START},{END})':eval=frame:format=auto[v1]"
        left="[v1][2:v]overlay=x='if(lt(t,20.55),NAN,if(lt(t,20.90),-430+(t-20.55)*1446,76))':y=354:eval=frame:format=auto[v2]"
        right="[v2][3:v]overlay=x='if(lt(t,20.85),NAN,if(lt(t,21.20),1080-(t-20.85)*1572,522))':y=354:eval=frame:format=auto[v]"
        args=['ffmpeg','-hide_banner','-loglevel','error','-y','-i',str(source)]
        for p in files:args+=['-loop','1','-framerate','30','-i',str(p)]
        args+=['-filter_complex',';'.join((bg,left,right)),'-map','[v]','-map','0:a:0','-c:v','libx264',
               '-preset','veryfast','-crf','20','-threads','4','-pix_fmt','yuv420p','-c:a','copy',
               '-movflags','+faststart','-t',str(before['duration']),str(output)]
        cmd(args)
    cmd(['ffmpeg','-v','error','-xerror','-i',str(output),'-f','null','-'])
    after=meta(output)
    sound_same=audio_digest(source)==audio_digest(output)
    passed=(after['frames']==before['frames']>0 and abs(after['duration']-before['duration'])<.05 and sound_same)
    result={'policy':POLICY,'genre':m['genre'],'source_sha256':digest(source),'output_sha256':digest(output),
            'before':before,'after':after,'full_av_decode':True,'aac_adts_bit_identical':sound_same,
            'technical_pass':passed,'changes':'scene8 procedural BEFORE/AFTER animated cards at 20.50-22.99s',
            'caption_semantics_verified':False,'japanese_asr_verified':False,
            'rights_approved':False,'employee_approved':False,'publication_approved':False}
    report.write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
    if not passed:
        output.unlink(missing_ok=True)
        raise RuntimeError('Technical QA failed; output removed')
    return result

if __name__=='__main__':
    p=argparse.ArgumentParser()
    for n in ('source','output','manifest','report'):p.add_argument('--'+n,required=True)
    a=p.parse_args()
    print(json.dumps(render(a.source,a.output,a.manifest,a.report),ensure_ascii=False,indent=2))
