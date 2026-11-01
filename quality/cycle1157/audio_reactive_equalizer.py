"""Cycle1157: replace decorative bars with audio-reactive narration-card bars.
No ASR, no auto posting, no media assets in repository.
"""
from __future__ import annotations
import argparse
import json
import subprocess
from pathlib import Path
import numpy as np
from PIL import Image, ImageDraw

PALETTES = {
    'ai-work': '#50d9cf', 'finance': '#f3c96b', 'career': '#76d6ac',
    'health': '#76d6b6', 'learning': '#6fbdff', 'travel': '#f5b47b',
    'technology': '#79baff', 'business': '#51d6d2', 'life': '#eeadd0',
    'history': '#dfb77d',
}
ICON_X, ICON_Y, ICON_W, ICON_H = 719, 1468, 124, 74
CAPTION_TEXT_MAX_X = 680

def call(args):
    return subprocess.run(args, check=True, capture_output=True)

def probe(path):
    return json.loads(call(['ffprobe','-v','error','-show_streams',
                            '-show_format','-of','json',str(path)]).stdout)

def validate_safe_region(x=ICON_X,y=ICON_Y,w=ICON_W,h=ICON_H,
                         text_max_x=CAPTION_TEXT_MAX_X,width=1080,height=1920):
    if min(x,y)<0 or min(w,h)<=0 or x+w>width or y+h>height:
        raise ValueError('Equalizer outside frame')
    if x<=text_max_x or y<1400 or y+h>1590:
        raise ValueError('Equalizer overlaps protected text/UI')
    return True

def extract_audio(source,sample_rate=48000):
    raw=call(['ffmpeg','-hide_banner','-loglevel','error','-i',str(source),
              '-map','0:a:0','-ac','1','-ar',str(sample_rate),
              '-f','f32le','-acodec','pcm_f32le','pipe:1']).stdout
    return np.frombuffer(raw,dtype='<f4').copy()

def compute_levels(audio,frames,fps=30,sample_rate=48000):
    if frames<=0 or fps<=0 or sample_rate<=0: raise ValueError('Invalid timing')
    bands=[(120,300),(300,600),(600,1000),(1000,1800),
           (1800,3000),(3000,5500),(5500,9000)]
    nfft=2048
    freq=np.fft.rfftfreq(nfft,1/sample_rate)
    masks=[(freq>=lo)&(freq<hi) for lo,hi in bands]
    raw=np.zeros((frames,7),np.float64)
    rms=np.zeros(frames,np.float64)
    for i in range(frames):
        start=int(i*sample_rate/fps);stop=int((i+1)*sample_rate/fps)
        chunk=audio[start:stop]
        if not len(chunk):continue
        rms[i]=np.sqrt(np.mean(chunk.astype(np.float64)**2))
        spec=np.abs(np.fft.rfft(chunk*np.hanning(len(chunk)),n=nfft))**2
        for b,mask in enumerate(masks):
            raw[i,b]=np.sqrt(np.mean(spec[mask])) if mask.any() else 0
    peaks=np.percentile(raw,97,axis=0)
    norm=np.clip(raw/np.maximum(peaks,1e-8),0,1)
    global_level=np.clip(rms/max(float(np.percentile(rms,97)),1e-8),0,1)
    combined=.70*global_level[:,None]+.30*norm
    smooth=np.zeros_like(combined)
    for i in range(frames):
        prev=smooth[i-1] if i else np.zeros(7)
        coeff=np.where(combined[i]>prev,.75,.42)
        smooth[i]=coeff*combined[i]+(1-coeff)*prev
    return np.clip(smooth,0,1),rms

def rgba_frame(levels,color='#50d9cf',width=ICON_W,height=ICON_H,visibility=1.0):
    if len(levels)!=7:raise ValueError('Expected seven bands')
    alpha=int(round(float(np.clip(visibility,0,1))*255))
    im=Image.new('RGBA',(width,height),(9,36,50,alpha))
    d=ImageDraw.Draw(im)
    for i,level in enumerate(levels):
        h=9+int(round(float(np.clip(level,0,1))*49))
        x=4+i*17;y=(height-h)//2
        d.rounded_rectangle((x,y,x+10,y+h),radius=5,
                            fill=(*tuple(bytes.fromhex(color.lstrip('#'))),alpha))
    return im

def extract_icon_visibility(source):
    raw=call(['ffmpeg','-v','error','-i',str(source),'-vf',
              f'crop={ICON_W}:{ICON_H}:{ICON_X}:{ICON_Y}',
              '-pix_fmt','rgb24','-f','rawvideo','pipe:1']).stdout
    frames=np.frombuffer(raw,dtype=np.uint8).reshape((-1,ICON_H,ICON_W,3))
    area=((frames[:,:,:,0]<160)&(frames[:,:,:,1]>130)&
          (frames[:,:,:,2]>125)).sum(axis=(1,2))
    return np.clip((area.astype(float)-100)/900,0,1)

def make_overlay_mov(levels,output,color,visibility=None):
    output=Path(output);output.parent.mkdir(parents=True,exist_ok=True)
    cmd=['ffmpeg','-hide_banner','-loglevel','error','-y',
         '-f','rawvideo','-pixel_format','rgba',
         '-video_size',f'{ICON_W}x{ICON_H}','-framerate','30','-i','pipe:0',
         '-c:v','qtrle','-pix_fmt','argb',str(output)]
    if visibility is None:visibility=np.ones(len(levels))
    if len(visibility)!=len(levels):raise ValueError('Visibility/frame mismatch')
    p=subprocess.Popen(cmd,stdin=subprocess.PIPE,stdout=subprocess.DEVNULL,
                       stderr=subprocess.PIPE)
    try:
        for row,vis in zip(levels,visibility):
            p.stdin.write(rgba_frame(row,color,visibility=vis).tobytes())
        p.stdin.close()
        err=p.stderr.read().decode(errors='replace')
        if p.wait()!=0:raise RuntimeError(err)
    finally:
        if p.poll() is None:p.kill();p.wait()
    return str(output)

def render(source,output,overlay_mov,genre='ai-work',preset='veryfast'):
    if genre not in PALETTES:raise ValueError('Unknown genre')
    validate_safe_region()
    info=probe(source)
    v=next(s for s in info['streams'] if s['codec_type']=='video')
    a=next((s for s in info['streams'] if s['codec_type']=='audio'),None)
    if a is None:raise ValueError('Existing audio required')
    if (int(v['width']),int(v['height']))!=(1080,1920):
        raise ValueError('Expected 1080x1920')
    fps=eval_fraction(v['avg_frame_rate'])
    if abs(fps-30)>.01:raise ValueError('Expected 30fps')
    frames=int(v.get('nb_frames') or round(float(info['format']['duration'])*30))
    levels,rms=compute_levels(extract_audio(source),frames)
    visibility=extract_icon_visibility(source)
    if len(visibility)!=frames:raise ValueError('Icon/video frame mismatch')
    make_overlay_mov(levels,overlay_mov,PALETTES[genre],visibility)
    # Dynamic alpha prevents floating bars during scene changes.
    filt=(f'[1:v]format=argb[eq];[0:v][eq]overlay={ICON_X}:{ICON_Y}:'
          'shortest=1:format=auto,format=yuv420p[v]')
    output=Path(output);output.parent.mkdir(parents=True,exist_ok=True)
    call(['ffmpeg','-hide_banner','-loglevel','error','-y','-i',str(source),
          '-i',str(overlay_mov),'-filter_complex',filt,
          '-map','[v]','-map','0:a:0','-map_metadata','0','-map_chapters','0',
          '-c:v','libx264','-crf','18','-preset',preset,'-pix_fmt','yuv420p',
          '-c:a','copy','-movflags','+faststart','-t',f'{frames/30:.3f}',
          str(output)])
    corr=float(np.corrcoef(levels.mean(axis=1),rms)[0,1]) if np.std(rms)>1e-8 else None
    return {'frames':frames,'duration_s':frames/30,'genre':genre,
            'genre_presets':len(PALETTES),'audio_rms_bar_correlation':corr,
            'icon_visible_frames':int((visibility>.5).sum()),
            'japanese_asr_verified':False,
            'subtitle_semantic_timing_verified':False,
            'publication_approved':False}

def eval_fraction(value):
    a,b=value.split('/')
    return float(a)/float(b)

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--source',required=True)
    ap.add_argument('--output',required=True)
    ap.add_argument('--overlay',required=True)
    ap.add_argument('--genre',default='ai-work',choices=tuple(PALETTES))
    ap.add_argument('--preset',default='veryfast')
    args=ap.parse_args()
    print(json.dumps(render(args.source,args.output,args.overlay,
                            args.genre,args.preset),indent=2))
if __name__=='__main__':main()
