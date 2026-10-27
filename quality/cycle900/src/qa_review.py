"""Private local technical QA for source and improved MP4; never uploads media."""
import argparse, hashlib, json, subprocess
from pathlib import Path

def command(*args):
    return subprocess.run(args, check=True, capture_output=True).stdout

def probe(path):
    return json.loads(command('ffprobe','-v','error','-show_entries',
        'format=duration,size:stream=index,codec_name,width,height,r_frame_rate,nb_frames,sample_rate,channels',
        '-of','json',str(path)))

def audio_sha(path):
    adts=command('ffmpeg','-v','error','-i',str(path),'-map','0:a:0',
                 '-c:a','copy','-f','adts','-')
    return hashlib.sha256(adts).hexdigest()

def compare_pixels(source, output):
    import cv2
    import numpy as np
    a=cv2.VideoCapture(str(source)); b=cv2.VideoCapture(str(output))
    cap_mae=[]; untouched=[]; changed=[]; count=0
    while True:
        ok1,f1=a.read();ok2,f2=b.read()
        if not ok1 and not ok2:break
        if not(ok1 and ok2):raise RuntimeError('frame count mismatch')
        if count%5==0:
            cap_mae.append(float(np.mean(cv2.absdiff(f1[1490:1700:4,90:990:4],f2[1490:1700:4,90:990:4]))))
            diff=float(np.mean(cv2.absdiff(f1[350:1370:8,70:1010:8],f2[350:1370:8,70:1010:8])))
            (changed if 348<=count<=434 else untouched).append(diff)
        count+=1
    a.release();b.release()
    return {'frames':count,'caption_mae_max':max(cap_mae),
            'untouched_mae_max':max(untouched),'scene05_mae_min':min(changed)}

def main():
    p=argparse.ArgumentParser()
    p.add_argument('source',type=Path)
    p.add_argument('output',type=Path)
    p.add_argument('--json',type=Path)
    a=p.parse_args()
    source=probe(a.source);out=probe(a.output)
    v=out['streams'][0];s=out['streams'][1]
    pixels=compare_pixels(a.source,a.output)
    command('ffmpeg','-v','error','-i',str(a.output),'-map','0:v:0',
            '-map','0:a:0','-f','null','-')
    checks={
        '1080x1920':(v['width'],v['height'])==(1080,1920),
        'h264_30fps':v['codec_name']=='h264' and v['r_frame_rate']=='30/1',
        'aac_48khz':s['codec_name']=='aac' and s['sample_rate']=='48000',
        'source_frame_count_preserved':int(v['nb_frames'])==int(source['streams'][0]['nb_frames'])==pixels['frames'],
        'full_decode':True,
        'audio_bitstream_preserved':audio_sha(a.source)==audio_sha(a.output),
        'caption_region_unchanged':pixels['caption_mae_max']<4,
        'other_scenes_unchanged':pixels['untouched_mae_max']<4,
        'scene05_visibly_changed':pixels['scene05_mae_min']>8,
    }
    result={'status':'HUMAN_REVIEW / PUBLICATION_NOT_APPROVED',
            'checks':checks,'measurements':pixels,
            'japanese_semantic_asr':'NOT_TESTED','rights':'UNVERIFIED',
            'phone_playback':'NOT_TESTED','employee_approval':False}
    if a.json:a.json.write_text(json.dumps(result,ensure_ascii=False,indent=2))
    print(json.dumps(result,ensure_ascii=False,indent=2))
    if not all(checks.values()):raise SystemExit(1)

if __name__=='__main__':main()
