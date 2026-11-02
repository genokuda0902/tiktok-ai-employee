#!/usr/bin/env python3
"""Offline original 10-genre Save/Reuse illustration for a vertical Japanese slide video.

Only replaces the center illustration in chapter 7. Existing narration,
subtitle panel, headers, footer and AAC bitstream remain untouched.
"""
from __future__ import annotations
import argparse
import hashlib
import json
import subprocess
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

W,H,FPS=1080,1920,30
ROI=(50,431,980,695)
PALETTES={
 'ai':'#55E4D2','business':'#70B9F6','money':'#E2C66F',
 'learning':'#9BC4F6','health':'#70D2B1','food':'#F4B280',
 'travel':'#80D5E5','beauty':'#ECA5CD','career':'#AAB4F7','life':'#A7D39A'
}
FONT='/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc'
BOLD='/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc'
SCENE_INDEX=6

def rgb(hexstr): return tuple(bytes.fromhex(hexstr.lstrip('#')))
def f(size,bold=False): return ImageFont.truetype(BOLD if bold else FONT, size)
def cmd(args):
    p=subprocess.run([str(a) for a in args],capture_output=True)
    if p.returncode: raise RuntimeError(p.stderr.decode(errors='replace')[-2000:])
    return p.stdout

def probe(path):
    return json.loads(cmd(['ffprobe','-v','error','-show_streams','-show_chapters','-show_format','-of','json',path]))
def stream(info,kind): return next(x for x in info['streams'] if x['codec_type']==kind)
def aac_sha(path):
    return hashlib.sha256(cmd(['ffmpeg','-v','error','-i',path,'-map','0:a:0','-c:a','copy','-f','adts','pipe:1'])).hexdigest()

def design(genre='ai',scale=2):
    if genre not in PALETTES: raise ValueError('Unsupported genre')
    if scale not in (1,2): raise ValueError('Scale must be 1 or 2')
    w,h=ROI[2]*scale,ROI[3]*scale
    accent=rgb(PALETTES[genre]); img=Image.new('RGBA',(w,h),(6,13,26,255));d=ImageDraw.Draw(img)
    boxes=[]
    def rect(xy,r,fill,outline=None,stroke=1):
        xy=tuple(int(v*scale) for v in xy)
        d.rounded_rectangle(xy,radius=int(r*scale),fill=fill,outline=outline,width=int(stroke*scale))
    def txt(x,y,s,size=30,color=(242,251,252),bold=False,max_x=None):
        ft=f(size*scale,bold)
        bbox=d.textbbox((int(x*scale),int(y*scale)),s,font=ft,stroke_width=0)
        if max_x is not None and bbox[2]>max_x*scale: raise ValueError(f'text overflows: {s}')
        if bbox[3]>h-5*scale: raise ValueError('text overflows bottom')
        d.text((x*scale,y*scale),s,font=ft,fill=color)
        boxes.append((s,tuple(round(v/scale) for v in bbox)))
    rect((2,2,978,693),25,(7,18,31,255),(*accent,130),2)
    rect((22,20,274,75),14,(12,60,70,255),(*accent,190),1)
    txt(39,28,'STEP 07 / SAVE',26,bold=True,max_x=270)
    txt(768,34,'実演・架空例',22,color=(184,212,223),max_x=950)
    txt(26,93,'一度つくった指示を、次回も使う',37,bold=True,max_x=956)
    rect((23,170,443,554),19,(11,27,43,255),(78,111,128,255),2)
    rect((537,170,957,554),19,(10,43,51,255),(*accent,215),2)
    rect((41,189,250,245),12,(18,67,76,255),(*accent,170),1)
    txt(57,199,'01  まとめる',27,bold=True,max_x=238)
    rect((555,189,785,245),12,(15,84,89,255),(*accent,170),1)
    txt(572,199,'02  保存する',27,bold=True,max_x=780)
    rows=[('目的','週次報告'),('条件','数字＋根拠'),('形式','箇条書き3点')]
    for i,(key,value) in enumerate(rows):
        top=268+i*88
        rect((42,top,423,top+70),11,(13,40,56,255),(55,83,101,255),1)
        txt(58,top+13,key,27,color=(141,220,220),bold=True,max_x=136)
        txt(157,top+11,value,29,bold=True,max_x=410)
    rect((558,268,937,474),14,(8,25,41,255),(57,101,114,255),2)
    txt(579,282,'保存ライブラリ',26,color=(181,231,235),bold=True,max_x=918)
    d.line((579*scale,331*scale,915*scale,331*scale),fill=(*accent,130),width=2*scale)
    txt(580,348,'週次報告テンプレート',29,bold=True,max_x=925)
    rect((579,412,739,459),12,(17,90,82,255),(*accent,190),1)
    txt(601,419,'✓ 保存済み',25,color=(222,255,242),bold=True,max_x=735)
    txt(570,493,'次回は選ぶだけ',25,color=(194,231,235),max_x=930)
    d.line((459*scale,350*scale,522*scale,350*scale),fill=(*accent,245),width=5*scale)
    d.polygon([(513*scale,338*scale),(531*scale,350*scale),(513*scale,362*scale)],fill=(*accent,245))
    rect((23,579,957,667),15,(12,72,74,255),(*accent,185),2)
    txt(50,595,'保存 → 再利用',34,color=(240,255,251),bold=True,max_x=383)
    txt(426,600,'毎回ゼロから書かない',30,color=(228,252,250),bold=True,max_x=930)
    return img,boxes

def panel(genre='ai'):
    image,_=design(genre,scale=2)
    image=image.resize((ROI[2],ROI[3]),Image.Resampling.LANCZOS)
    overlay=Image.new('RGBA',(W,H),(0,0,0,0))
    overlay.alpha_composite(image,(ROI[0],ROI[1]))
    return overlay

def render(source,output,genre='ai',report=None):
    source=Path(source);output=Path(output)
    if not source.is_file() or source.resolve()==output.resolve(): raise ValueError('Invalid source/output')
    info=probe(source); v=stream(info,'video');a=stream(info,'audio')
    if (v['codec_name'],v['width'],v['height'],v['r_frame_rate'],a['codec_name'])!=('h264',W,H,'30/1','aac'):
        raise ValueError('Source must be H264 1080x1920 30fps with AAC')
    if len(info['chapters'])!=8: raise ValueError('Expected eight chapters')
    chapter=info['chapters'][SCENE_INDEX];start=float(chapter['start_time']);end=float(chapter['end_time'])
    if not 2.0<end-start<4.0: raise ValueError('Unexpected chapter 7 duration')
    frames=int(v['nb_frames']); output.parent.mkdir(parents=True,exist_ok=True)
    overlay=output.parent/(output.stem+'_overlay.png');panel(genre).save(overlay)
    last=end-1/FPS
    cmd(['ffmpeg','-hide_banner','-loglevel','error','-y','-i',source,
         '-loop','1','-framerate',FPS,'-i',overlay,
         '-filter_complex',f"[0:v][1:v]overlay=0:0:enable='between(t,{start:.3f},{last:.3f})':format=auto[v]",
         '-map','[v]','-map','0:a:0','-map_chapters','0',
         '-c:v','libx264','-preset','medium','-crf','21','-x264-params','aq-mode=3:aq-strength=1.0',
         '-pix_fmt','yuv420p','-frames:v',frames,'-c:a','copy','-movflags','+faststart',output])
    out=probe(output);ov=stream(out,'video')
    if (ov['width'],ov['height'],ov['r_frame_rate'],int(ov['nb_frames']))!=(W,H,'30/1',frames): raise RuntimeError('Video geometry changed')
    if aac_sha(source)!=aac_sha(output): raise RuntimeError('AAC changed')
    if len(out['chapters'])!=len(info['chapters']): raise RuntimeError('Chapter count changed')
    cmd(['ffmpeg','-v','error','-xerror','-i',output,'-map','0:v:0','-map','0:a:0','-f','null','-'])
    qa={'cycle':1239,'previous_cycle':1237,'change':'Chapter 7 original save/reuse infographic replaces crowded overlapping library UI',
        'genre':genre,'genres_supported':len(PALETTES),'resolution':[W,H],'fps':FPS,'frames':frames,
        'chapters':len(out['chapters']),'duration_s':float(out['format']['duration']),
        'source_bytes':source.stat().st_size,'output_bytes':output.stat().st_size,
        'audio_aac_sha256':aac_sha(output),'audio_bitstream_identical':True,'full_av_decode':'PASS',
        'chapter7_interval_s':[start,end],'subtitle_semantics':'NOT VERIFIED: independent Japanese ASR unavailable',
        'source_rights':'NOT VERIFIED','reference_v33':'NOT ACCESSIBLE','employee_approval':'NOT GRANTED',
        'publication':'HUMAN_REVIEW / PUBLICATION_NOT_APPROVED'}
    if report: Path(report).write_text(json.dumps(qa,ensure_ascii=False,indent=2),encoding='utf-8')
    return qa

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--source',required=True);p.add_argument('--output',required=True)
    p.add_argument('--genre',default='ai',choices=sorted(PALETTES));p.add_argument('--report')
    args=p.parse_args();print(json.dumps(render(args.source,args.output,args.genre,args.report),ensure_ascii=False))
