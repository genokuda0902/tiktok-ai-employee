"""Zero-cost review-only 10-genre voice-reactive header for Japanese image-slide videos.
The meter uses the ACTUAL AAC audio, not random animation. No ASR or publishing.
"""
from __future__ import annotations
import argparse, hashlib, json, subprocess, tempfile
from pathlib import Path
import numpy as np
from PIL import Image, ImageDraw

GENRE_COLORS = {
    'ai_work': (45,213,197), 'business': (118,186,255),
    'finance': (229,187,105), 'education': (243,172,117),
    'career': (155,184,255), 'wellness': (135,212,161),
    'lifestyle': (231,166,205), 'technology': (90,197,232),
    'travel': (226,185,142), 'trivia': (199,165,240),
}
REVIEWED_GENRES={'ai_work'}
METER_BOX=(565,70,715,111)
SR=16000
FPS=30

def run(args,capture=False,timeout=300):
    p=subprocess.run(args,stdout=subprocess.PIPE if capture else subprocess.DEVNULL,
                     stderr=subprocess.PIPE,timeout=timeout,check=False)
    if p.returncode:
        raise RuntimeError(f'{args[0]} exit={p.returncode}: {p.stderr.decode(errors="replace")[-1500:]}')
    return p.stdout if capture else None

def sha256(path):
    h=hashlib.sha256()
    with open(path,'rb') as f:
        for part in iter(lambda:f.read(1<<20),b''):h.update(part)
    return h.hexdigest()

def probe(path):
    return json.loads(run(['ffprobe','-v','error','-show_streams','-show_format','-of','json',str(path)],capture=True))

def check_media(info,genre,synthetic_test=False):
    if genre not in GENRE_COLORS:raise ValueError('Unknown genre')
    if genre not in REVIEWED_GENRES:raise PermissionError('Genre has not passed placement review')
    video=next((x for x in info['streams'] if x['codec_type']=='video'),None)
    audio=next((x for x in info['streams'] if x['codec_type']=='audio'),None)
    if not video or not audio:raise ValueError('Video and audio required')
    if (video['codec_name'],video['width'],video['height'],video['r_frame_rate'])!=('h264',1080,1920,'30/1'):
        raise ValueError('Only H264 1080x1920 30fps has reviewed header placement')
    if audio['codec_name']!='aac' or int(audio['sample_rate'])!=48000:
        raise ValueError('Japanese AAC 48kHz source required')
    duration=float(info['format']['duration'])
    if not synthetic_test and not 22.9<=duration<=23.1:
        raise ValueError('Unreviewed source duration')
    return duration

def read_audio(path):
    raw=run(['ffmpeg','-hide_banner','-loglevel','error','-i',str(path),
             '-vn','-ac','1','-ar',str(SR),'-f','f32le','pipe:1'],capture=True,timeout=90)
    return np.frombuffer(raw,dtype='<f4').copy()

def analyze_audio(samples,frame_count):
    if not len(samples) or not np.isfinite(samples).all():
        raise ValueError('Empty/nonfinite audio')
    centers=(np.arange(frame_count)+.5)*SR/FPS
    bands=np.geomspace(170,3900,9)
    freqs=np.fft.rfftfreq(1024,1/SR)
    window=np.hanning(1024).astype(np.float32)
    power=np.zeros((frame_count,8),dtype=np.float32)
    rms=np.zeros(frame_count,dtype=np.float32)
    for i,c in enumerate(centers):
        start=int(c)-512
        src0,src1=max(0,start),min(len(samples),start+1024)
        segment=np.zeros(1024,dtype=np.float32)
        if src1>src0:segment[src0-start:src1-start]=samples[src0:src1]
        rms[i]=float(np.sqrt(np.mean(segment*segment)))
        spec=np.abs(np.fft.rfft(segment*window))
        for j in range(8):
            idx=(freqs>=bands[j])&(freqs<bands[j+1])
            power[i,j]=float(np.sqrt(np.mean(spec[idx]**2))) if idx.any() else 0
    lo=np.percentile(power,15,axis=0)
    hi=np.percentile(power,92,axis=0)
    values=np.clip((power-lo)/(hi-lo+1e-6),0,1)
    rlo,rhi=np.percentile(rms,[10,90])
    gate=np.clip((rms-rlo)/(rhi-rlo+1e-6),0,1)
    values*=(.18+.82*gate[:,None])
    for i in range(1,frame_count):
        a=np.where(values[i]>values[i-1],.68,.35)
        values[i]=a*values[i]+(1-a)*values[i-1]
    return values,rms

def draw_meter(levels,color):
    w,h=METER_BOX[2]-METER_BOX[0],METER_BOX[3]-METER_BOX[1]
    im=Image.new('RGBA',(w,h),(0,0,0,0))
    d=ImageDraw.Draw(im)
    d.rounded_rectangle((0,0,w-1,h-1),radius=8,fill=(7,22,42,255))
    for i,v in enumerate(levels):
        height=4+int(round(23*float(v)))
        x=10+i*17
        top=(h-height)//2
        d.rounded_rectangle((x,top,x+7,top+height),radius=3,fill=(*color,240))
    return im

def render(source,target,report_path,genre='ai_work',synthetic_test=False):
    source,target,report_path=map(Path,(source,target,report_path))
    if source.resolve()==target.resolve():raise ValueError('Refuse in-place modification')
    duration=check_media(probe(source),genre,synthetic_test)
    count=round(duration*FPS)
    audio=read_audio(source)
    levels,rms=analyze_audio(audio,count)
    target.parent.mkdir(parents=True,exist_ok=True)
    with tempfile.TemporaryDirectory(prefix='cycle967_meter_') as td:
        for i,v in enumerate(levels):
            draw_meter(v,GENRE_COLORS[genre]).save(f'{td}/frame_{i:04d}.png')
        run(['ffmpeg','-hide_banner','-loglevel','error','-y',
             '-i',str(source),'-framerate','30','-i',f'{td}/frame_%04d.png',
             '-filter_complex','[0:v:0][1:v:0]overlay=565:70:shortest=1:format=auto,format=yuv420p[v]',
             '-map','[v]','-map','0:a:0','-c:v','libx264','-preset','veryfast',
             '-crf','18','-pix_fmt','yuv420p','-c:a','copy',
             '-metadata:s:a:0','language=jpn','-movflags','+faststart',
             '-t',f'{count/FPS:.6f}',str(target)],timeout=300)
    report={'cycle':967,'source_sha256':sha256(source),'output_sha256':sha256(target),
            'source_duration_s':duration,'frames_expected':count,
            'audio_samples':len(audio),'audio_rms_min':round(float(rms.min()),5),
            'audio_rms_max':round(float(rms.max()),5),
            'meter_levels_min':round(float(levels.min()),4),
            'meter_levels_max':round(float(levels.max()),4),
            'meter_bbox':list(METER_BOX),'genre':genre,
            'improvement':'8 frequency-band VOICE bars from actual AAC audio',
            'independent_japanese_asr':'NOT_VERIFIED',
            'rights':'INHERITED_MEDIA_RIGHTS_NOT_VERIFIED',
            'publish_approved':False,'manual_employee_approval_required':True}
    report_path.parent.mkdir(parents=True,exist_ok=True)
    report_path.write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
    return report

def main():
    p=argparse.ArgumentParser()
    p.add_argument('--input',required=True)
    p.add_argument('--output',required=True)
    p.add_argument('--report',required=True)
    p.add_argument('--genre',default='ai_work',choices=sorted(GENRE_COLORS))
    p.add_argument('--synthetic-test',action='store_true',help='Only for synthetic CI fixtures')
    a=p.parse_args()
    print(json.dumps(render(a.input,a.output,a.report,a.genre,a.synthetic_test),ensure_ascii=False))

if __name__=='__main__':main()
