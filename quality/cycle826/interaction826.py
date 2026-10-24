"""cycle826: original animated, fictional prompt-to-result demonstration.
Review only. No real service screens, personal data, private assets, auto-posting.
A common 10-genre compositor overlays only the upper scene; subtitles stay intact.
"""
from __future__ import annotations
import argparse
import hashlib
import json
import subprocess
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

GENRES = ('ai_work','beauty','love_psychology','money_saving','sales_business',
          'career','health_life','science','travel_food','product_life')
PALETTES = {'ai_work':'#19B9D4','beauty':'#E36FA9','love_psychology':'#B889D8',
 'money_saving':'#22A477','sales_business':'#25AFC5','career':'#5C83D6',
 'health_life':'#59AD82','science':'#7288E0','travel_food':'#E79C52',
 'product_life':'#B695D0'}
WIDTH,HEIGHT,FPS=952,648,30
SCENE_START,SCENE_END=9.687,12.917
REGION=(64,482,WIDTH,HEIGHT)
PROMPT='週報を200字で要約して。\n対象：架空の営業日報。\n形式：要点3つ＋次の行動。'
SAMPLE=('1  実績の変化を確認','2  課題を一つ選ぶ','3  次の行動を決める')
FONT_PATH='/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc'
BOLD_PATH='/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc'

def font(size:int,bold:bool=False):
    return ImageFont.truetype(BOLD_PATH if bold else FONT_PATH,size)

def gate(genre:str,start:float=SCENE_START,end:float=SCENE_END):
    if genre not in GENRES: raise ValueError('unknown genre')
    if not (0<=start<end<=60 and end-start>=2.5): raise ValueError('unsafe scene timing')
    x,y,w,h=REGION
    if x<50 or x+w>1030 or y<420 or y+h>1190:raise ValueError('subtitle-safe region failed')
    if len(PROMPT)>100 or not all('架空' not in x for x in SAMPLE):raise ValueError('demo text invalid')

def make_frame(progress:float,genre:str='ai_work')->Image.Image:
    gate(genre)
    p=max(0,min(1,progress));accent=PALETTES[genre]
    im=Image.new('RGB',(WIDTH,HEIGHT),'#F3F8FA');d=ImageDraw.Draw(im)
    d.rounded_rectangle((4,4,WIDTH-5,HEIGHT-5),radius=30,fill='#F7FAFC',outline='#D8E8EF',width=4)
    d.rounded_rectangle((5,5,WIDTH-6,83),radius=26,fill='#173A4C')
    d.rectangle((5,59,WIDTH-6,83),fill='#173A4C')
    for j,c in enumerate(('#F27877','#E7C264','#65D1A6')):d.ellipse((32+j*32,32,49+j*32,49),fill=c)
    d.text((143,41),'AI WORKSPACE  /  DEMO',font=font(27,True),fill='#FFFFFF',anchor='lm')
    d.text((WIDTH-34,42),'架空の操作例',font=font(23),fill='#C8E3EA',anchor='rm')
    d.text((40,124),'指示を書く → 実行 → 結果を確認',font=font(39,True),fill='#183C4E')
    d.rounded_rectangle((32,189,567,579),radius=20,fill='#FFFFFF',outline='#D3E4EA',width=3)
    d.text((60,227),'入力する指示',font=font(29,True),fill='#264C60')
    d.rounded_rectangle((56,273,541,485),radius=16,fill='#F0F7FA')
    chars=int(len(PROMPT)*min(1,p/0.53))
    typed=PROMPT[:chars]
    for i,line in enumerate(typed.split('\n')):
        d.text((76,302+i*58),line,font=font(26),fill='#183D50')
    if p<0.53 and int(p*24)%2==0:
        lines=typed.split('\n');last=lines[-1]
        cursor_x=76+int(d.textlength(last,font=font(26)))
        d.rectangle((cursor_x,303+58*(len(lines)-1),cursor_x+3,340+58*(len(lines)-1)),fill=accent)
    button=('#0B8D9F' if p>=0.55 else '#79B6C1')
    d.rounded_rectangle((377,509,535,562),radius=13,fill=button)
    d.text((455,535),'実行 ✓' if p>=0.55 else '実行 →',font=font(26,True),fill='white',anchor='mm')
    d.rounded_rectangle((585,189,918,579),radius=20,fill='#FFFFFF',outline='#D3E4EA',width=3)
    d.text((608,227),'出力プレビュー',font=font(28,True),fill='#264C60')
    if p<0.58:
        d.text((616,340),'入力を待っています',font=font(23),fill='#8A9DA8')
    elif p<0.70:
        d.text((616,340),'要点を整理中…',font=font(25),fill='#557B89')
        for i in range(3):
            d.ellipse((622+i*35,391,635+i*35,404),fill=accent)
    else:
        n=min(3,1+int((p-0.70)/0.10))
        for i,s in enumerate(SAMPLE[:n]):
            yy=316+i*75
            d.rounded_rectangle((603,yy-24,895,yy+35),radius=10,fill='#EAF5F6')
            d.text((618,yy),s,font=font(22,True),fill='#18465A',anchor='lm')
        d.text((606,552),'※内容・数値は架空の例です',font=font(18),fill='#617F8B')
    d.rounded_rectangle((32,603,920,625),radius=10,fill='#D9E8EE')
    d.rounded_rectangle((32,603,32+int(888*p),625),radius=10,fill=accent)
    return im

def probe(path:Path):
    return json.loads(subprocess.check_output(['ffprobe','-v','error','-show_streams','-show_format','-of','json',str(path)]))

def audio_md5(path:Path)->str:
    return subprocess.check_output(['ffmpeg','-v','error','-i',str(path),'-map','0:a:0','-c','copy','-f','md5','-']).decode().strip()

def render(source:Path,output:Path,genre:str='ai_work',start:float=SCENE_START,end:float=SCENE_END)->dict:
    gate(genre,start,end)
    if not source.is_file():raise FileNotFoundError(source)
    meta=probe(source);v=next(s for s in meta['streams'] if s['codec_type']=='video')
    a=next(s for s in meta['streams'] if s['codec_type']=='audio')
    duration=float(meta['format']['duration'])
    if (v['width'],v['height'])!=(1080,1920) or v['r_frame_rate']!='30/1' or a['codec_name']!='aac':
        raise ValueError('expected 1080x1920 30fps H264/AAC source')
    if end>duration:raise ValueError('insert past source duration')
    n=round((end-start)*FPS)
    output.parent.mkdir(parents=True,exist_ok=True)
    filter_complex=(f"[0:v][1:v]overlay=x={REGION[0]}:y={REGION[1]}:"
      f"eof_action=pass:shortest=0:enable='between(t,{start:.3f},{end:.3f})',format=yuv420p[v]")
    cmd=['ffmpeg','-hide_banner','-loglevel','error','-y','-i',str(source),
      '-itsoffset',f'{start:.6f}','-f','rawvideo','-pixel_format','rgb24',
      '-video_size',f'{WIDTH}x{HEIGHT}','-framerate',str(FPS),'-i','pipe:0',
      '-filter_complex',filter_complex,'-map','[v]','-map','0:a:0',
      '-frames:v',str(v['nb_frames']),'-c:v','libx264','-preset','ultrafast',
      '-crf','22','-threads','4','-pix_fmt','yuv420p','-c:a','copy',
      '-movflags','+faststart',str(output)]
    proc=subprocess.Popen(cmd,stdin=subprocess.PIPE,stderr=subprocess.PIPE)
    try:
        for i in range(n):
            im=make_frame(i/max(1,n-1),genre)
            proc.stdin.write(im.tobytes())
        proc.stdin.close()
        error=proc.stderr.read().decode(errors='replace')
        if proc.wait()!=0:raise RuntimeError('ffmpeg failed: '+error[-2000:])
    except BaseException:
        proc.kill();proc.wait();raise
    result=probe(output)
    vv=next(s for s in result['streams'] if s['codec_type']=='video')
    aa=next(s for s in result['streams'] if s['codec_type']=='audio')
    checks={'1080x1920_30fps':(vv['width'],vv['height'],vv['r_frame_rate'])==(1080,1920,'30/1'),
      'frame_count_preserved':int(vv['nb_frames'])==int(v['nb_frames']),
      'h264_aac_48k':vv['codec_name']=='h264' and aa['codec_name']=='aac' and aa['sample_rate']=='48000',
      'audio_bitstream_identical':audio_md5(source)==audio_md5(output),
      'full_decode':subprocess.run(['ffmpeg','-v','error','-xerror','-i',str(output),'-f','null','-'],capture_output=True).returncode==0}
    return {'cycle':826,'genre':genre,'scene':[start,end],'frames_changed':n,
      'checks':checks,'sha256':hashlib.sha256(output.read_bytes()).hexdigest(),
      'reference_v33_direct_comparison':False,'audible_japanese_semantics_verified':False,
      'word_level_subtitle_sync_verified':False,'smartphone_verified':False,
      'publication_approved':False,'review_only':True,'auto_post':False}

if __name__=='__main__':
    p=argparse.ArgumentParser()
    p.add_argument('--source',type=Path,required=True);p.add_argument('--output',type=Path,required=True)
    p.add_argument('--genre',choices=GENRES,default='ai_work')
    p.add_argument('--start',type=float,default=SCENE_START);p.add_argument('--end',type=float,default=SCENE_END)
    p.add_argument('--report',type=Path)
    a=p.parse_args();report=render(a.source,a.output,a.genre,a.start,a.end)
    if a.report:a.report.write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
    print(json.dumps(report,ensure_ascii=False,indent=2))
    if not all(report['checks'].values()):raise SystemExit('QA failed')
