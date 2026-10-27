"""Cycle885 review-only kinetic task cards for ten genre templates.

Private source video, audio and review manifest must never be committed or uploaded.
"""
import argparse
import hashlib
import json
import re
import subprocess
from dataclasses import dataclass
from pathlib import Path

GENRES = ('ai_productivity','beauty','romance_psychology','money_saving',
          'sales_business','career','health_lifestyle','trivia_science',
          'travel_food','product_lifestyle')
CANVAS=(1080,1920)
FPS=30
TOTAL_FRAMES=691
CAPTION_TOP=1438
START=89
END=170
POLICY = {'review_only':True,'publication_approved':False,
          'external_upload':False,'automatic_posting':False,
          'source_rights_reviewed':False,'synthetic_ui':True}
DEMO_TASKS=('月別データを集計','同じ表を毎週更新','転記と数字の照合')

@dataclass(frozen=True)
class Story:
    genre: str
    heading: str
    tasks: tuple[str,str,str]
    cta: str

DEMO=Story('ai_productivity','繰り返し作業を見つける',DEMO_TASKS,'まずは1つ、書き出そう')

def sha256(path):
    h=hashlib.sha256()
    with open(path,'rb') as f:
        for chunk in iter(lambda:f.read(1024*1024),b''):h.update(chunk)
    return h.hexdigest()

def validate_story(story, width=1080, height=1920, caption_top=CAPTION_TOP):
    if story.genre not in GENRES:raise ValueError('unrecognized genre')
    if width<540 or height<960 or caption_top>height-300 or caption_top<600:
        raise ValueError('invalid portrait safe region')
    if len(story.tasks)!=3 or len(set(story.tasks))!=3:
        raise ValueError('three distinct tasks required')
    for s in (story.heading,*story.tasks,story.cta):
        if not s or len(s)>24 or re.search(r'[\r\n\t<>]|@|https?://|\d{2,}[- ]?\d{3,}',s):
            raise ValueError('unsafe or overflowing on-screen copy')
    return True

def validate_manifest(manifest,source):
    if any(manifest.get(k)!=v for k,v in POLICY.items()):
        raise ValueError('unsafe publication/source policy')
    if manifest.get('source_sha256')!=sha256(source):
        raise ValueError('source sha256 mismatch')
    return True

def ease_out(t):
    t=max(0.,min(1.,float(t)))
    return 1-(1-t)**3

def card_phase(local_frame,index):
    begins=(8,27,46)
    start=begins[index]
    if local_frame<start:return 0.,0
    t=ease_out((local_frame-start+1)/12)
    return t,round((1-t)*115)

def draw_frame(local_frame,story=DEMO,font_path='/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc'):
    from PIL import Image,ImageDraw,ImageFont
    validate_story(story)
    if not 0<=local_frame<END-START:raise ValueError('frame outside scene')
    W,H=CANVAS[0],CAPTION_TOP
    im=Image.new('RGBA',(W,H),(0,0,0,0))
    d=ImageDraw.Draw(im,'RGBA')
    font=lambda size: ImageFont.truetype(font_path,size,index=0)
    d.rounded_rectangle((35,250,1045,1430),radius=45,fill=(7,20,42,255),
                        outline=(26,126,155,240),width=3)
    d.rounded_rectangle((65,285,360,338),radius=20,fill=(13,110,139,230))
    d.text((91,290),'STEP 01 / FIND',font=font(27),fill=(227,249,255,255))
    d.text((80,382),story.heading,font=font(60),fill=(255,255,255,255))
    d.line((82,476,996,476),fill=(36,181,212,170),width=3)
    colors=((21,189,212),(42,145,240),(239,186,83))
    for idx,txt in enumerate(story.tasks):
        a,offset=card_phase(local_frame,idx)
        if a<=0:continue
        top=540+idx*192
        left=80+offset
        alpha=round(a*255)
        d.rounded_rectangle((left,top,995+offset,top+154),radius=28,
                            fill=(17,47,73,round(255*a)),
                            outline=(*colors[idx],round(210*a)),width=3)
        d.rounded_rectangle((left+20,top+27,left+120,top+127),radius=25,
                            fill=(*colors[idx],alpha))
        d.text((left+48,top+48),str(idx+1),font=font(51),fill=(255,255,255,alpha))
        d.text((left+153,top+44),txt,font=font(46),fill=(247,252,255,alpha))
        if local_frame>=66 and idx==2:
            d.rounded_rectangle((left+855,top+49,left+892,top+87),radius=15,
                                fill=(95,231,175,alpha))
    if local_frame>=68:
        a=ease_out((local_frame-68+1)/10)
        d.rounded_rectangle((80,1165,995,1290),radius=30,
                            fill=(12,113,139,round(235*a)))
        d.text((151,1193),story.cta,font=font(43),
               fill=(255,255,255,round(255*a)))
    return im

def generate_overlays(folder,story=DEMO):
    folder=Path(folder);folder.mkdir(parents=True,exist_ok=True)
    for f in range(END-START):
        draw_frame(f,story).save(folder/f'{f:03d}.png',compress_level=1)
    return END-START

def probe(path):
    return json.loads(subprocess.check_output(['ffprobe','-v','error',
      '-show_entries','format=duration:stream=codec_name,codec_type,width,height,r_frame_rate,nb_frames,sample_rate,channels',
      '-of','json',str(path)],text=True))

def render(source,output,manifest_path,report_path,work_dir):
    source=Path(source);output=Path(output)
    validate_manifest(json.loads(Path(manifest_path).read_text()),source)
    meta=probe(source)
    v=next(x for x in meta['streams'] if x['codec_type']=='video')
    a=next(x for x in meta['streams'] if x['codec_type']=='audio')
    if (v['width'],v['height'],v['r_frame_rate'],int(v['nb_frames']),a['codec_name'])!=(1080,1920,'30/1',691,'aac'):
        raise ValueError('unverified source stream')
    generate_overlays(work_dir)
    output.parent.mkdir(parents=True,exist_ok=True)
    fg=f"[1:v]setpts=PTS+{START}/({FPS}*TB)[ov];[0:v][ov]overlay=x=0:y=0:shortest=0:repeatlast=0:eof_action=pass:format=auto:enable='between(n,{START},{END-1})'[v]"
    cmd=['ffmpeg','-hide_banner','-loglevel','error','-y','-i',str(source),
         '-framerate','30','-start_number','0','-i',str(Path(work_dir)/'%03d.png'),
         '-filter_complex',fg,'-map','[v]','-map','0:a:0',
         '-frames:v','691','-c:v','libx264','-preset','veryfast','-crf','19',
         '-pix_fmt','yuv420p','-c:a','copy','-movflags','+faststart',str(output)]
    subprocess.run(cmd,check=True,timeout=300)
    subprocess.run(['ffmpeg','-v','error','-xerror','-i',str(output),
                    '-map','0:v:0','-map','0:a:0','-f','null','-'],check=True,timeout=120)
    result={'cycle':885,'source_sha256':sha256(source),'output_sha256':sha256(output),
            'target_frames':[START,END-1],'changed_scene':'02 / task selection',
            'audio_preserved':'COPY','full_av_decode':'PASS',
            'independent_japanese_asr':'UNVERIFIED',
            'semantic_caption_alignment':'UNVERIFIED',
            'source_rights':'UNVERIFIED','phone_playback':'UNVERIFIED',
            'release':'HUMAN_REVIEW / PUBLICATION_NOT_APPROVED'}
    Path(report_path).write_text(json.dumps(result,ensure_ascii=False,indent=2))
    return result

if __name__=='__main__':
    p=argparse.ArgumentParser()
    for k in ('source','output','manifest','report','work-dir'):
        p.add_argument('--'+k,required=True)
    a=p.parse_args()
    print(json.dumps(render(a.source,a.output,a.manifest,a.report,a.work_dir),
                     ensure_ascii=False,indent=2))
