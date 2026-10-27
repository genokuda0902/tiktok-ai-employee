"""Review-only narration-reactive accent, shared across ten genres.

Audio activity, not transcription: this cannot establish Japanese word accuracy.
No private source/audio/frames should be committed to public GitHub.
"""
from __future__ import annotations
import argparse, hashlib, json, math, struct, subprocess, zlib
from pathlib import Path
from array import array

FPS=30
FRAMES=691
SAMPLE_RATE=16000
WIDTH,HEIGHT=160,54
Y=1405
GENRES=('ai_productivity','beauty','romance_psychology','money_saving',
        'sales_business','career','health_lifestyle','trivia_science',
        'travel_food','product_lifestyle')
POLICY={'review_only':True,'publication_approved':False,'external_upload':False,
        'automatic_posting':False,'source_rights_reviewed':False}

def sha256(path):
    h=hashlib.sha256()
    with open(path,'rb') as f:
        for block in iter(lambda:f.read(1024*1024),b''):
            h.update(block)
    return h.hexdigest()

def validate_manifest(m):
    if not isinstance(m,dict) or any(m.get(k) is not v for k,v in POLICY.items()):
        raise ValueError('Fail-closed review policy required')
    if m.get('genre') not in GENRES or m.get('real_service_footage') is not False or m.get('reference_equivalent') is not False:
        raise ValueError('Invalid genre or unsupported claims')
    h=m.get('source_sha256')
    if not isinstance(h,str) or len(h)!=64 or any(c not in '0123456789abcdef' for c in h):
        raise ValueError('Exact source SHA256 required')
    return True

def probe(path):
    return json.loads(subprocess.check_output(['ffprobe','-v','error','-show_entries',
        'format=duration:stream=codec_type,codec_name,width,height,r_frame_rate,nb_frames,sample_rate,channels',
        '-of','json',str(path)],text=True))

def validate_media(path):
    p=probe(path)
    v=next(x for x in p['streams'] if x['codec_type']=='video')
    a=next(x for x in p['streams'] if x['codec_type']=='audio')
    if (v['codec_name'],v['width'],v['height'],v['r_frame_rate'],int(v['nb_frames']))!=('h264',1080,1920,'30/1',FRAMES):
        raise ValueError('Unexpected video geometry')
    if (a['codec_name'],int(a['sample_rate']),a['channels'])!=('aac',48000,2):
        raise ValueError('Unexpected audio stream')
    return p

def extract_envelope(path):
    raw=subprocess.check_output(['ffmpeg','-v','error','-i',str(path),'-vn','-ac','1',
        '-ar',str(SAMPLE_RATE),'-f','s16le','-acodec','pcm_s16le','-'])
    samples=array('h'); samples.frombytes(raw)
    step=SAMPLE_RATE/FPS
    values=[]
    for i in range(FRAMES):
        s=int(i*step); e=min(len(samples),int((i+1)*step))
        values.append(math.sqrt(sum(float(x)*x for x in samples[s:e])/max(e-s,1))/32768)
    return values

def smooth_envelope(values):
    if len(values)!=FRAMES or not all(math.isfinite(x) and x>=0 for x in values):
        raise ValueError('Need 691 finite nonnegative RMS samples')
    positive=sorted(v for v in values if v>0)
    ref=positive[min(len(positive)-1,int(len(positive)*0.9))] if positive else 1
    ref=max(ref,0.0001)
    out=[]; previous=0.0
    for v in values:
        target=min(1.,max(0.,v/ref))
        previous+=(0.42 if target>previous else 0.18)*(target-previous)
        out.append(previous)
    return out

def bars(levels,i):
    if not (0<=i<len(levels)):
        raise ValueError('Frame out of range')
    return [max(4,min(32,round(4+28*levels[max(0,i-d)]*scale)))
            for d,scale in zip((8,4,0,3,7),(0.65,0.88,1.,0.84,0.60))]

def png_chunk(tag,data):
    return struct.pack('>I',len(data))+tag+data+struct.pack('>I',zlib.crc32(tag+data)&0xffffffff)

def write_png(path,bar_heights):
    if len(bar_heights)!=5 or any(not 4<=h<=32 for h in bar_heights):
        raise ValueError('Invalid visualizer heights')
    pixels=bytearray(WIDTH*HEIGHT*4)
    def rect(x0,y0,x1,y1,color):
        for y in range(y0,y1):
            for x in range(x0,x1):
                k=(y*WIDTH+x)*4
                pixels[k:k+4]=bytes(color)
    rect(0,3,WIDTH,HEIGHT-3,(4,17,33,170))
    for j,h in enumerate(bar_heights):
        x=25+j*27
        rect(x,HEIGHT-8-h,x+12,HEIGHT-8,(67,221,238,215))
    raw=b''.join(b'\x00'+pixels[y*WIDTH*4:(y+1)*WIDTH*4] for y in range(HEIGHT))
    path.write_bytes(b'\x89PNG\r\n\x1a\n'+png_chunk(b'IHDR',struct.pack('>IIBBBBB',WIDTH,HEIGHT,8,6,0,0,0))+
                     png_chunk(b'IDAT',zlib.compress(raw,6))+png_chunk(b'IEND',b''))

def render(source,output,manifest,work,report):
    source,output,manifest,work,report=map(Path,(source,output,manifest,work,report))
    m=json.loads(manifest.read_text(encoding='utf-8'))
    validate_manifest(m)
    if sha256(source)!=m['source_sha256']:
        raise ValueError('Source SHA mismatch')
    validate_media(source)
    levels=smooth_envelope(extract_envelope(source))
    work.mkdir(parents=True,exist_ok=True); output.parent.mkdir(parents=True,exist_ok=True)
    for i in range(FRAMES):
        write_png(work/f'pulse_{i:04d}.png',bars(levels,i))
    cmd=['ffmpeg','-hide_banner','-loglevel','error','-y','-i',str(source),
         '-framerate',str(FPS),'-start_number','0','-i',str(work/'pulse_%04d.png'),
         '-filter_complex',f'[0:v][1:v]overlay=860:{Y}:format=auto:shortest=1,format=yuv420p[v]',
         '-map','[v]','-map','0:a:0','-frames:v',str(FRAMES),
         '-c:v','libx264','-preset','veryfast','-crf','19','-pix_fmt','yuv420p',
         '-c:a','copy','-movflags','+faststart',str(output)]
    subprocess.run(cmd,check=True,timeout=300)
    validate_media(output)
    subprocess.run(['ffmpeg','-v','error','-xerror','-i',str(output),'-f','null','-'],check=True,timeout=120)
    r={'cycle':898,'source_sha256':sha256(source),'output_sha256':sha256(output),
       'changed_effect':'narration-responsive 5-bar accent, 691 frames, safe y1405-1459',
       'active_frame_count':sum(v>0.20 for v in levels),
       'min_bar_height':min(min(bars(levels,i)) for i in range(FRAMES)),
       'max_bar_height':max(max(bars(levels,i)) for i in range(FRAMES)),
       'audio_stream_copy':True,'full_av_decode':'PASS','genre':m['genre'],
       'review_only':True,'publication_approved':False,
       'independent_japanese_asr':'UNVERIFIED','caption_semantic_match':'UNVERIFIED',
       'source_rights':'UNVERIFIED','smartphone_playback':'UNVERIFIED'}
    report.write_text(json.dumps(r,ensure_ascii=False,indent=2),encoding='utf-8')
    return r

if __name__=='__main__':
    ap=argparse.ArgumentParser()
    for name in ('source','output','manifest','work','report'):
        ap.add_argument('--'+name,required=True)
    a=ap.parse_args()
    print(json.dumps(render(a.source,a.output,a.manifest,a.work,a.report),ensure_ascii=False))
