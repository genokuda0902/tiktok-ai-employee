"""Local private MP4 technical QA; never commit private media to GitHub."""
import argparse,json,subprocess
from pathlib import Path
import numpy as np

def run(cmd):
    return subprocess.run(cmd,check=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE,timeout=180).stdout

def probe(path):
    return json.loads(run(['ffprobe','-v','error','-show_entries','format=duration,size:stream=index,codec_name,codec_type,width,height,avg_frame_rate,nb_frames,sample_rate,channels:stream_tags=language','-of','json',str(path)]))

def vhash(path):
    return run(['ffmpeg','-v','error','-i',str(path),'-map','0:v:0','-c','copy','-f','hash','-hash','sha256','-']).decode().strip()

def pcm(path):
    return np.frombuffer(run(['ffmpeg','-v','error','-i',str(path),'-map','0:a:0','-ac','2','-ar','48000','-f','f32le','-acodec','pcm_f32le','-']),dtype='<f4').reshape(-1,2)

def verify(source,output):
    import sound_cue_engine as e
    e.validate(source)
    a,b=probe(source),probe(output)
    av=[s for s in a['streams'] if s['codec_type']=='video'][0]
    bv=[s for s in b['streams'] if s['codec_type']=='video'][0]
    ba=[s for s in b['streams'] if s['codec_type']=='audio'][0]
    assert av['codec_name']==bv['codec_name']=='h264'
    assert (bv['width'],bv['height'],bv['nb_frames'],bv['avg_frame_rate'])==(1080,1920,'691','30/1')
    assert abs(float(b['format']['duration'])-691/30)<.01
    assert (ba['codec_name'],ba['sample_rate'],ba['channels'])==('aac','48000',2)
    assert ba['tags']['language']=='jpn'
    h1,h2=vhash(source),vhash(output)
    assert h1==h2,'video elementary stream changed (burned captions at risk)'
    run(['ffmpeg','-v','error','-xerror','-i',str(output),'-map','0:v:0','-map','0:a:0','-f','null','-'])
    x,y=pcm(source),pcm(output)
    assert x.shape==y.shape
    d=y-x
    rms=lambda z:float(np.sqrt(np.mean(z*z)))
    outside=rms(d[int(3*48000):int(3.5*48000)])
    changes={}
    for name,sec,_,_,dur in e.EVENTS:
        val=rms(d[int((sec+.015)*48000):int((sec+dur-.015)*48000)])
        assert val>outside*8, f'missing audible {name} cue'
        changes[name]=round(val,7)
    peak=float(np.max(abs(y)))
    assert peak<0.9,'unsafe output peak'
    corr=float(np.corrcoef(x[::100,0],y[::100,0])[0,1]);assert corr>0.995
    return {'source_sha256':e.sha256(source),'output_sha256':e.sha256(output),
            'video_stream_hash':h2,'video_unchanged':True,
            'format':{'codec':'H.264/AAC','resolution':'1080x1920','fps':30,'frames':691,'duration_seconds':float(b['format']['duration']),'audio_sample_rate':48000,'audio_channels':2,'audio_language_tag':'jpn'},
            'full_video_audio_decode':'PASS','pcm_correlation':round(corr,6),
            'difference_rms_outside_cues':round(outside,7),
            'difference_rms_at_cues':changes,'output_pcm_peak':round(peak,6),
            'original_sound_effects_only':True,
            'independent_Japanese_ASR':'NOT_PERFORMED','caption_speech_semantics':'NOT_VERIFIED',
            'phone_playback':'NOT_VERIFIED','rights_and_employee_approval':'NOT_VERIFIED',
            'publication':'HUMAN_REVIEW / PUBLICATION_NOT_APPROVED'}

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--source',required=True);p.add_argument('--output',required=True);p.add_argument('--qa',required=True);a=p.parse_args()
    result=verify(Path(a.source),Path(a.output))
    Path(a.qa).write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
    print(json.dumps(result,ensure_ascii=False))
