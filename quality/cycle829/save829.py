"""cycle829: fictional reusable-prompt save/reuse visual, review only.

The renderer works on an existing 1080x1920 H264/AAC review video.
No external media, real application screenshot, PII, posting or publication approval.
"""
from __future__ import annotations
import argparse, hashlib, json, math, subprocess, tempfile
from functools import lru_cache
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageFilter

GENRES=('ai_work','beauty','love_psychology','money_saving','sales_business',
        'career','health_life','science','travel_food','product_life')
PALETTES={'ai_work':'#20C3DB','beauty':'#E36FA9','love_psychology':'#B889D8',
          'money_saving':'#22A477','sales_business':'#25AFC5','career':'#5C83D6',
          'health_life':'#59AD82','science':'#7288E0','travel_food':'#E79C52',
          'product_life':'#B695D0'}
FPS=30
START,END=19.383,22.617
X,Y,W,H=64,482,952,648
FONT='/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc'
BOLD='/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc'
NOTICE='架空の画面・個人情報や実サービスの操作は含みません'
PHASES=('よく使う指示を選ぶ','名前を付けて保存','次回も再利用できる')

def validate(genre='ai_work',start=START,end=END):
    if genre not in GENRES:raise ValueError('unknown genre')
    if abs(start-START)>.001 or abs(end-END)>.001:raise ValueError('unexpected scene window')
    if not (X>=48 and X+W<=1032 and Y>=420 and Y+H<=1170):raise ValueError('caption safe region')
    if len(PHASES)!=3 or '架空' not in NOTICE:raise ValueError('review-only provenance')
    return True

def font(n,bold=False):return ImageFont.truetype(BOLD if bold else FONT,n)

def lerp(a,b,t):return a+(b-a)*max(0,min(1,t))

def smooth(t):
    t=max(0,min(1,t));return t*t*(3-2*t)

@lru_cache(maxsize=1)
def background():
    # Original desk illustration with spatial depth, warm window light and texture.
    import numpy as np
    yy,xx=np.mgrid[0:H,0:W]
    grain=np.sin(xx*.047+yy*.012)*2.8+np.sin(xx*.009+yy*.12)*2.3
    sun=np.exp(-((xx-790)**2/(2*340**2)+(yy-110)**2/(2*310**2)))*64
    shade=np.clip(1-(xx*.00030+yy*.00040),.48,1)
    rgb=np.stack([np.clip((92+sun+grain)*shade,0,255),
                  np.clip((65+sun*.66+grain)*shade,0,255),
                  np.clip((49+sun*.36+grain)*shade,0,255)],axis=-1).astype('uint8')
    im=Image.fromarray(rgb,'RGB');d=ImageDraw.Draw(im)
    d.rounded_rectangle((62,52,632,564),radius=25,fill='#342D2A')
    d.rounded_rectangle((75,42,619,550),radius=20,fill='#DCCBAF')
    d.rounded_rectangle((99,63,602,531),radius=15,fill='#F8F1E2')
    for y in range(158,515,39):d.line((132,y,573,y),fill='#D1D9D1',width=2)
    d.line((175,101,175,514),fill='#E2AAA0',width=3)
    d.rounded_rectangle((510,52,551,119),radius=16,outline='#A6B2B2',width=7)
    d.line((672,448,826,295),fill='#0D2E40',width=19)
    d.line((679,448,831,292),fill='#C8A65A',width=5)
    d.ellipse((738,64,900,226),fill='#342C26')
    d.ellipse((754,77,885,208),fill='#E8D8B8')
    d.ellipse((767,90,872,195),fill='#3D271F')
    return im

def frame(progress,genre='ai_work'):
    validate(genre)
    p=max(0.,min(1.,float(progress)))
    accent=PALETTES[genre]
    base=background()
    zoom=1+0.023*smooth(p)
    if zoom>1:
        zw,zh=round(W*zoom),round(H*zoom)
        expanded=base.resize((zw,zh),Image.Resampling.BICUBIC)
        ox=round((zw-W)*.59);oy=round((zh-H)*.42)
        base=expanded.crop((ox,oy,ox+W,oy+H))
    d=ImageDraw.Draw(base)
    d.rounded_rectangle((135,84,560,149),radius=16,fill='#173A47')
    d.text((155,117),'指示テンプレート',font=font(33,True),fill='#FFFFFF',anchor='lm')
    d.text((147,208),'例：日報を3行で要約して',font=font(27,True),fill='#273C41',anchor='lm')
    d.text((147,264),'重要な点と次の行動を',font=font(27),fill='#385159',anchor='lm')
    d.text((147,308),'分けて整理してください。',font=font(27),fill='#385159',anchor='lm')
    stage=0 if p<.33 else 1 if p<.68 else 2
    if stage>=1:
        alpha=smooth((p-.33)/.15)
        ribbon=Image.new('RGBA',(W,H));rd=ImageDraw.Draw(ribbon)
        rd.rounded_rectangle((366,353,569,427),radius=17,fill=(18,89,93,int(230*alpha)))
        rd.text((467,390),'✓ 保存',font=font(33,True),fill=(255,255,255,int(255*alpha)),anchor='mm')
        base=Image.alpha_composite(base.convert('RGBA'),ribbon).convert('RGB');d=ImageDraw.Draw(base)
    if stage>=2:
        d.rounded_rectangle((602,250,918,422),radius=22,fill='#143F4B',outline=accent,width=5)
        d.text((761,299),'次回も使える',font=font(30,True),fill='white',anchor='mm')
        d.text((761,351),'テンプレート',font=font(32,True),fill=accent,anchor='mm')
        d.text((761,392),'✓ 再利用OK',font=font(24,True),fill='white',anchor='mm')
    else:
        d.rounded_rectangle((635,276,905,407),radius=19,fill='#183743')
        d.text((770,326),'保存して',font=font(28,True),fill='white',anchor='mm')
        d.text((770,368),'次回も使おう',font=font(25,True),fill=accent,anchor='mm')
    d.rounded_rectangle((20,560,932,633),radius=14,fill='#0E2E3A')
    d.text((47,587),PHASES[stage],font=font(29,True),fill='white',anchor='lm')
    d.text((910,588),f'{stage+1}/3',font=font(25,True),fill=accent,anchor='rm')
    d.text((476,616),NOTICE,font=font(16),fill='#BBD1D4',anchor='mm')
    return base

def probe(path):
    return json.loads(subprocess.check_output(['ffprobe','-v','error','-show_streams','-show_format','-of','json',str(path)]))

def audio_md5(path):
    return subprocess.check_output(['ffmpeg','-v','error','-i',str(path),'-map','0:a:0','-c','copy','-f','md5','-']).decode().strip()

def audio_rms(path):
    # Check for an actual non-silent audio stream; not a Japanese speech transcript.
    import re
    r=subprocess.run(['ffmpeg','-hide_banner','-nostats','-i',str(path),'-map','0:a:0',
                      '-af','volumedetect','-f','null','-'],capture_output=True,text=True)
    m=re.search(r'mean_volume:\s*(-?[0-9.]+) dB',r.stderr)
    return float(m.group(1)) if r.returncode==0 and m else None

def render(source:Path,output:Path,genre='ai_work'):
    validate(genre)
    if not source.is_file():raise FileNotFoundError(source)
    info=probe(source);v=next(s for s in info['streams'] if s['codec_type']=='video')
    a=next(s for s in info['streams'] if s['codec_type']=='audio')
    if (v['width'],v['height'],v['r_frame_rate'],v['codec_name'])!=(1080,1920,'30/1','h264') or a['codec_name']!='aac':raise ValueError('invalid source media')
    if float(info['format']['duration'])<END:raise ValueError('source too short')
    n=round((END-START)*FPS)
    output.parent.mkdir(parents=True,exist_ok=True)
    with tempfile.TemporaryDirectory(prefix='cycle829_') as td:
        td=Path(td);overlay=td/'scene829.mp4'
        for i in range(n):frame(i/max(1,n-1),genre).save(td/f'frame_{i:03}.jpg',quality=93)
        subprocess.run(['ffmpeg','-hide_banner','-loglevel','error','-y','-framerate',str(FPS),
                        '-i',str(td/'frame_%03d.jpg'),'-frames:v',str(n),'-c:v','libx264',
                        '-preset','ultrafast','-crf','19','-threads','4','-pix_fmt','yuv420p',str(overlay)],check=True,capture_output=True)
        filt=f"[0:v][1:v]overlay=x={X}:y={Y}:shortest=1:enable='between(t,{START:.3f},{END:.3f})',format=yuv420p[v]"
        subprocess.run(['ffmpeg','-hide_banner','-loglevel','error','-y','-i',str(source),
                        '-stream_loop','-1','-itsoffset',f'{START:.6f}','-i',str(overlay),
                        '-filter_complex',filt,'-map','[v]','-map','0:a:0',
                        '-frames:v',str(v['nb_frames']),'-c:v','libx264','-preset','ultrafast',
                        '-crf','22','-threads','4','-pix_fmt','yuv420p','-c:a','copy',
                        '-movflags','+faststart',str(output)],check=True,capture_output=True)
    o=probe(output);vv=next(s for s in o['streams'] if s['codec_type']=='video')
    aa=next(s for s in o['streams'] if s['codec_type']=='audio')
    mean=audio_rms(output)
    checks={'1080x1920_30fps':(vv['width'],vv['height'],vv['r_frame_rate'])==(1080,1920,'30/1'),
      '775_frames':int(vv['nb_frames'])==int(v['nb_frames'])==775,
      'h264_aac_48k':vv['codec_name']=='h264' and aa['codec_name']=='aac' and aa['sample_rate']=='48000',
      'audio_packets_preserved':audio_md5(source)==audio_md5(output),
      'audible_level_not_silent':mean is not None and -45<mean<0,
      'full_av_decode':subprocess.run(['ffmpeg','-v','error','-xerror','-i',str(output),'-f','null','-'],capture_output=True).returncode==0}
    return {'cycle':829,'previous':828,'scene_seconds':[START,END], 'frames_changed':n,
      'genre':genre,'checks':checks,'audio_mean_db':mean,'sha256':hashlib.sha256(output.read_bytes()).hexdigest(),
      'asset_provenance':'original_procedural_fictional', 'speech_semantics_independently_verified':False,
      'word_level_subtitle_sync_verified':False,'reference_v33_compared':False,
      'smartphone_verified':False,'publication_approved':False,'auto_post':False,'review_only':True}

if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--source',type=Path,required=True)
    ap.add_argument('--output',type=Path,required=True)
    ap.add_argument('--genre',choices=GENRES,default='ai_work');ap.add_argument('--report',type=Path)
    args=ap.parse_args();result=render(args.source,args.output,args.genre)
    if args.report:
        args.report.parent.mkdir(parents=True,exist_ok=True)
        args.report.write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
    print(json.dumps(result,ensure_ascii=False,indent=2))
    if not all(result['checks'].values()):raise SystemExit(1)
