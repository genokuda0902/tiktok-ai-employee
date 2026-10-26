"""Private local QA: stream integrity, audio identity, subtitle-zone stability."""
from pathlib import Path
import subprocess,json,hashlib,cv2,numpy as np
from evidence_montage import probe,digest,START,N,TOTAL,ROI

def adts_hash(path, temp):
    subprocess.run(['ffmpeg','-hide_banner','-loglevel','error','-y','-i',str(path),'-map','0:a:0','-c:a','copy','-f','adts',str(temp)],check=True,timeout=80)
    return digest(temp)

def frame_at(path,frame):
    cap=cv2.VideoCapture(str(path));cap.set(cv2.CAP_PROP_POS_FRAMES,frame)
    ok,img=cap.read();cap.release()
    if not ok:raise RuntimeError(f'cannot read frame {frame} from {path}')
    return img

def verify(src,out,work):
    src,out=Path(src),Path(out);work=Path(work)
    streams=probe(out)['streams'];v=next(s for s in streams if s['codec_type']=='video')
    a=next(s for s in streams if s['codec_type']=='audio')
    # Full video and audio decode (not just metadata)
    subprocess.run(['ffmpeg','-hide_banner','-loglevel','error','-xerror','-i',str(out),'-f','null','-'],check=True,timeout=150)
    aa=adts_hash(src,work/'source_audio.adts');bb=adts_hash(out,work/'output_audio.adts')
    samples=[]
    for i in (104,124,145,161):
        p=frame_at(src,i);q=frame_at(out,i)
        # Burned Japanese caption panel is below y=1490; no intentional changes.
        caption_delta=float(np.mean(np.abs(p[1490:1840].astype(np.int16)-q[1490:1840].astype(np.int16))))
        x,y,w,h=ROI
        region_delta=float(np.mean(np.abs(p[y:y+h,x:x+w].astype(np.int16)-q[y:y+h,x:x+w].astype(np.int16))))
        samples.append({'frame':i,'picture_delta':round(region_delta,3),'caption_delta':round(caption_delta,3)})
    outside=frame_at(src,375);outside2=frame_at(out,375)
    outside_delta=float(np.mean(np.abs(outside.astype(np.int16)-outside2.astype(np.int16))))
    checks={'resolution':(v['width'],v['height'])==(1080,1920),'video_codec':v['codec_name']=='h264',
            'frame_count':int(v['nb_frames'])==TOTAL,'frame_rate':v['r_frame_rate']=='30/1',
            'audio_codec':a['codec_name']=='aac','audio_sample_rate':a['sample_rate']=='48000',
            'full_av_decode':True,'audio_elementary_identity':aa==bb,
            'caption_protected':all(x['caption_delta']<2.0 for x in samples),
            'visual_change_present':all(x['picture_delta']>15 for x in samples),
            'outside_scene_stable':outside_delta<3.0,
            'duration':abs(float(probe(out)['format']['duration'])-23.033333)<.04}
    result={'checks':checks,'passed':sum(checks.values()),'total':len(checks),
            'source_sha256':digest(src),'output_sha256':digest(out),
            'audio_adts_sha256':bb,'samples':samples,'outside_delta':round(outside_delta,3),
            'note':'Audio byte identity is NOT Japanese semantic/phonetic verification; smartphone/rights/employee approval pending.'}
    (work/'verification861.json').write_text(json.dumps(result,ensure_ascii=False,indent=2))
    if not all(checks.values()):raise AssertionError(result)
    return result

if __name__=='__main__':
    import sys
    print(json.dumps(verify(sys.argv[1],sys.argv[2],sys.argv[3]),ensure_ascii=False,indent=2))