"""Review-only 10-genre UI focus overlay. Original reimplementation, not recovered v33."""
import argparse,hashlib,json,subprocess,tempfile
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont,ImageFilter
GENRES=('ai_productivity','finance','career','business','education','lifestyle','science','travel','health','entertainment')
FONT='/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc'

def run(cmd):
    p=subprocess.run([str(c) for c in cmd],text=True,capture_output=True)
    if p.returncode: raise RuntimeError(' '.join(map(str,cmd))+'\n'+p.stderr[-4000:])
    return p.stdout

def intersect(a,b):
    x,y,w,h=a;X,Y,W,H=b
    return max(0,min(x+w,X+W)-max(x,X))*max(0,min(y+h,Y+H)-max(y,Y))

def validate(c):
    if c.get('mode')!='review_only' or c.get('rights_reviewed') is not False or c.get('publication_approved') is not False:
        raise ValueError('FAIL CLOSED: rights/publication status')
    if c.get('genre') not in GENRES or set(c.get('genres',[]))!=set(GENRES):
        raise ValueError('missing genre presets')
    w,h=c['canvas'];margin=c.get('safe_margin',0.05)
    if (w,h)!=(1080,1920) or not 0.04<=margin<=0.12: raise ValueError('bad canvas/margin')
    scenes=c['focus_events'];duration=c['duration_seconds']
    if len(scenes)!=2: raise ValueError('need input and send focus')
    for s in scenes:
        if not 0<=s['start']<s['end']<=duration: raise ValueError('invalid time')
        x,y,bw,bh=s['box']
        if not all(type(v) is int for v in (x,y,bw,bh)) or not (w*margin<=x and h*margin<=y and bw>0 and bh>0 and x+bw<=w*(1-margin) and y+bh<=h*(1-margin)):
            raise ValueError('unsafe focus box')
        if intersect(s['box'],c['protected_caption_box']):raise ValueError('focus collides with caption')
    if scenes[0]['end']>scenes[1]['start']:raise ValueError('focus overlap')
    return True

def make_overlay(box,kind,path,canvas=(1080,1920)):
    w,h=canvas;x,y,bw,bh=box
    im=Image.new('RGBA',(w,h),(0,0,0,0))
    halo=Image.new('RGBA',(w,h),(0,0,0,0));d=ImageDraw.Draw(halo)
    d.rounded_rectangle((x-8,y-8,x+bw+8,y+bh+8),radius=26,outline=(30,255,225,180),width=16)
    im=Image.alpha_composite(im,halo.filter(ImageFilter.GaussianBlur(20)))
    d=ImageDraw.Draw(im)
    d.rounded_rectangle((x,y,x+bw,y+bh),radius=20,outline=(45,255,226,235),width=8)
    if kind=='input':
        font=ImageFont.truetype(FONT,34)
        d.rounded_rectangle((x+16,y-59,x+288,y-10),radius=12,fill=(0,47,63,237),outline=(36,233,220,220),width=2)
        d.text((x+32,y-56),'ここに指示を入力',font=font,fill=(255,255,255,255))
    else:
        px,py=x+bw-28,y+bh-15
        pts=[(px,py),(px+12,py+47),(px+23,py+34),(px+44,py+65),(px+57,py+56),(px+36,py+25),(px+56,py+22)]
        d.polygon(pts,fill=(255,255,255,250))
        d.line(pts+[pts[0]],fill=(2,24,34,255),width=4,joint='curve')
    im.save(path)
    return path

def probe(path):
    p=json.loads(run(['ffprobe','-v','error','-show_entries','format=duration:stream=codec_type,codec_name,width,height,nb_frames,r_frame_rate','-of','json',path]))
    streams=p['streams'];v=next((s for s in streams if s['codec_type']=='video'),None);a=next((s for s in streams if s['codec_type']=='audio'),None)
    if not v or not a or v['width']!=1080 or v['height']!=1920:raise ValueError('invalid audio/video or dimensions')
    return p

def render(cfg,src,dst,report):
    validate(cfg)
    src=Path(src);dst=Path(dst)
    if not src.is_file():raise FileNotFoundError(src)
    if 'REVIEW_ONLY' not in dst.name:raise ValueError('must be review only')
    source_probe=probe(src)
    if abs(float(source_probe['format']['duration'])-cfg['duration_seconds'])>0.07:raise ValueError('duration mismatch')
    dst.parent.mkdir(parents=True,exist_ok=True)
    with tempfile.TemporaryDirectory() as tmp:
        imgs=[make_overlay(s['box'],kind,Path(tmp)/(kind+'.png')) for kind,s in zip(('input','send'),cfg['focus_events'])]
        first,second=cfg['focus_events']
        filt=(f"[0:v][1:v]overlay=0:0:format=auto:enable='between(t,{first['start']},{first['end']})'[v1];"
              f"[v1][2:v]overlay=0:0:format=auto:enable='between(t,{second['start']},{second['end']})',format=yuv420p[vout]")
        video_only=Path(tmp)/'video_only.mp4'
        run(['ffmpeg','-hide_banner','-loglevel','error','-y','-i',src,
             '-loop','1','-framerate','30','-i',imgs[0],'-loop','1','-framerate','30','-i',imgs[1],
             '-filter_complex',filt,'-map','[vout]',
             '-c:v','libx264','-preset','veryfast','-crf','19','-pix_fmt','yuv420p',
             '-an','-frames:v',str(int(next(s for s in source_probe['streams'] if s['codec_type']=='video')['nb_frames'])),video_only])
        # Remux inherited AAC separately to preserve the final packet and original duration.
        run(['ffmpeg','-hide_banner','-loglevel','error','-y','-i',video_only,'-i',src,
             '-map','0:v:0','-map','1:a:0','-c:v','copy','-c:a','copy','-movflags','+faststart',dst])
    result=probe(dst)
    run(['ffmpeg','-v','error','-i',dst,'-f','null','-'])
    stats={'cycle':794,'source_duration':float(source_probe['format']['duration']),
           'output_duration':float(result['format']['duration']),
           'frames':int(next(s for s in result['streams'] if s['codec_type']=='video')['nb_frames']),
           'sha256':hashlib.sha256(dst.read_bytes()).hexdigest(),
           'audio_codec':next(s for s in result['streams'] if s['codec_type']=='audio')['codec_name'],
           'events':cfg['focus_events'],'status':'HUMAN_REVIEW',
           'publication_approved':False,'rights_reviewed':False,
           'japanese_narration_semantics_verified':False,'phone_playback_verified':False}
    Path(report).parent.mkdir(parents=True,exist_ok=True)
    Path(report).write_text(json.dumps(stats,ensure_ascii=False,indent=2),encoding='utf-8')
    return stats

if __name__=='__main__':
    p=argparse.ArgumentParser()
    for k in ('config','input','output','report'):p.add_argument('--'+k,required=True)
    a=p.parse_args()
    print(json.dumps(render(json.loads(Path(a.config).read_text(encoding='utf-8')),a.input,a.output,a.report),ensure_ascii=False))
