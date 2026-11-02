#!/usr/bin/env python3
"""Review-only 3-beat task visualization, independent of v33 source.

Uses only original offline Pillow vectors; never uploads or embeds source media.
The Japanese narration and burned-in captions are inherited, not transcribed.
"""
import argparse
import hashlib
import json
import subprocess
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

POLICY = 'HUMAN_REVIEW/PUBLICATION_NOT_APPROVED'
PALETTES = {'ai':'2BE2D2','business':'F0C171','money':'7ED6A1',
            'learning':'B4A2F8','health':'83DAC9','food':'FFC48D',
            'travel':'86CEFF','beauty':'F2A7D7','career':'F2D181','life':'A2D7AE'}
STAGES = [(3.00,3.96),(3.96,4.92),(4.92,5.96)]
TASKS = [('01','データの集計','毎日、数字をまとめる'),
         ('02','報告メール','同じ内容を整える'),
         ('03','資料の整形','見た目をそろえる')]
OVERLAY_HEIGHT = 1270
FONT = '/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc'
BOLD = '/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc'


def run(args):
    p = subprocess.run([str(a) for a in args], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if p.returncode:
        raise RuntimeError(p.stderr.decode(errors='replace')[-2200:])
    return p.stdout


def sha(path):
    h=hashlib.sha256()
    with open(path,'rb') as f:
        for chunk in iter(lambda:f.read(1024*1024),b''):h.update(chunk)
    return h.hexdigest()


def meta(path):
    j=json.loads(run(['ffprobe','-v','error','-show_streams','-show_format','-of','json',path]))
    v=next(s for s in j['streams'] if s['codec_type']=='video')
    a=next(s for s in j['streams'] if s['codec_type']=='audio')
    return {'duration':float(j['format']['duration']),'frames':int(v.get('nb_frames') or 0),
            'width':v['width'],'height':v['height'],'fps':v['avg_frame_rate'],
            'video':v['codec_name'],'audio':a['codec_name'],
            'sample_rate':int(a['sample_rate']),'language':a.get('tags',{}).get('language','und')}


def audio_sha(path):
    return hashlib.sha256(run(['ffmpeg','-v','error','-i',path,'-map','0:a:0','-c:a','copy','-f','adts','pipe:1'])).hexdigest()


def validate(manifest, source):
    required={'policy':POLICY,'asset_approval':'review_only_no_publication',
              'manual_post_only':True,'roi_reviewed':True,'genre':manifest.get('genre'),
              'overlay_height':OVERLAY_HEIGHT,'source_sha256':sha(source)}
    if any(manifest.get(k)!=v for k,v in required.items()):
        raise ValueError('Fail closed: manifest approval, bounds or hash mismatch')
    if manifest['genre'] not in PALETTES:raise ValueError('Unknown genre')
    m=meta(source)
    if (m['width'],m['height'],m['fps'],m['video'],m['audio'],m['sample_rate']) != (1080,1920,'30/1','h264','aac',48000):
        raise ValueError('Expected 1080x1920 H264 30fps AAC48k')
    if m['duration']<6.0:raise ValueError('Source too short for stage 3')
    if OVERLAY_HEIGHT>=1400:raise ValueError('Subtitle safety boundary violated')
    return m


def font(path,size):return ImageFont.truetype(path,size)


def panel(genre, selected):
    """Generate a source-independent original visual; no photos/screenshots."""
    if genre not in PALETTES or selected not in range(3):raise ValueError('Invalid stage')
    accent='#'+PALETTES[genre]
    im=Image.new('RGB',(1080,OVERLAY_HEIGHT),'#050D1D')
    d=ImageDraw.Draw(im)
    for y in range(OVERLAY_HEIGHT):
        shade=int(10+15*y/OVERLAY_HEIGHT)
        d.line((0,y,1080,y),fill=(5,shade,31+int(y/180)))
    for i in range(7):
        x=70+i*150
        d.line((x,0,x-80,OVERLAY_HEIGHT),fill='#142339',width=2)
    d.rounded_rectangle((60,70,1020,1200),radius=38,fill='#0B1A2D',outline='#2B4865',width=3)
    d.text((96,100),'STEP 02 / 08',font=font(BOLD,30),fill=accent)
    d.text((95,165),'毎日の作業を',font=font(BOLD,70),fill='#F5F9FF')
    d.text((95,255),'見える化しよう',font=font(BOLD,70),fill='#F5F9FF')
    d.line((95,367,985,367),fill='#2B4961',width=3)
    for i,(num,title,desc) in enumerate(TASKS):
        y=408+i*206
        active=i==selected
        fill='#163B48' if active else '#102337'
        stroke=accent if active else '#294259'
        d.rounded_rectangle((95,y,985,y+178),radius=25,fill=fill,outline=stroke,width=5 if active else 2)
        d.rounded_rectangle((120,y+31,210,y+122),radius=20,fill=accent if active else '#2B4256')
        d.text((140,y+48),num,font=font(BOLD,40),fill='#071323' if active else '#CFDBE7')
        d.text((238,y+25),title,font=font(BOLD,49),fill='#FFFFFF' if active else '#C5D3E2')
        d.text((240,y+100),desc,font=font(FONT,30),fill='#D0E4E8' if active else '#8DA8BD')
        if active:
            d.ellipse((922,y+66,949,y+93),fill=accent)
    d.rounded_rectangle((95,1050,985,1155),radius=20,fill='#0E3040')
    d.text((131,1073),'まず1つ選んで、AIで試す',font=font(BOLD,41),fill='#FFFFFF')
    return im


def graph():
    g='[0:v]format=yuv420p[b];'
    last='b'
    for i,(start,end) in enumerate(STAGES):
        next_label=f'v{i}'
        g+=f'[{last}][{i+1}:v]overlay=x=0:y=0:enable=\'gte(t,{start})*lt(t,{end})\':eof_action=repeat:format=auto[{next_label}];'
        last=next_label
    return g+f'[{last}]format=yuv420p[v]'


def render(source,output,manifest_path,report_path):
    source,output,manifest_path,report_path=map(Path,(source,output,manifest_path,report_path))
    if not source.is_file() or source.resolve()==output.resolve():raise ValueError('Missing source or same output')
    manifest=json.loads(manifest_path.read_text(encoding='utf-8'))
    before=validate(manifest,source)
    output.parent.mkdir(parents=True,exist_ok=True)
    stills=[]
    for i in range(3):
        p=output.parent/f'_cycle1174_stage{i}.png'
        panel(manifest['genre'],i).save(p,optimize=True)
        stills.append(p)
    args=['ffmpeg','-hide_banner','-loglevel','error','-y','-i',source]
    for p in stills:args+=['-loop','1','-framerate','30','-i',p]
    args+=['-filter_complex',graph(),'-map','[v]','-map','0:a:0','-c:v','libx264',
           '-preset','veryfast','-crf','20','-threads','4','-pix_fmt','yuv420p',
           '-c:a','copy','-movflags','+faststart','-t',f"{before['duration']:.6f}",output]
    try:
        run(args)
        run(['ffmpeg','-v','error','-xerror','-i',output,'-f','null','-'])
        after=meta(output)
        same=audio_sha(source)==audio_sha(output)
        ok=same and before['frames']==after['frames'] and abs(before['duration']-after['duration'])<0.05
        report={'policy':POLICY,'source_sha256':sha(source),'output_sha256':sha(output),
                'genre':manifest['genre'],'before':before,'after':after,
                'stages':STAGES,'overlay_height':OVERLAY_HEIGHT,
                'audio_adts_bit_identical':same,'full_av_decode':True,'technical_pass':ok,
                'japanese_asr_verified':False,'subtitle_meaning_timing_verified':False,
                'smartphone_verified':False,'rights_approved':False,
                'employee_approved':False,'publication_approved':False}
        report_path.parent.mkdir(parents=True,exist_ok=True)
        report_path.write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
        if not ok:
            output.unlink(missing_ok=True)
            raise RuntimeError('Technical verification failed')
        return report
    finally:
        for p in stills:p.unlink(missing_ok=True)

if __name__=='__main__':
    a=argparse.ArgumentParser()
    for k in ('source','output','manifest','report'):a.add_argument('--'+k,required=True)
    q=a.parse_args()
    print(json.dumps(render(q.source,q.output,q.manifest,q.report),ensure_ascii=False,indent=2))
