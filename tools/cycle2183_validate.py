#!/usr/bin/env python3
import json, subprocess, sys

def validate(path):
    p = subprocess.run(['ffprobe','-v','error','-show_streams','-show_format','-of','json',path],capture_output=True,text=True,check=True)
    data=json.loads(p.stdout); streams=data['streams']
    video=next((s for s in streams if s['codec_type']=='video'),None)
    assert video and video['codec_name']=='h264' and (video['width'],video['height'])==(1080,1920), 'vertical H264 missing'
    assert any(s['codec_type']=='audio' for s in streams), 'Japanese narration missing: NOT APPROVED'
    subprocess.run(['ffmpeg','-v','error','-i',path,'-f','null','-'],check=True)
    return True

if __name__=='__main__':
    try: validate(sys.argv[1]); print('PASS')
    except Exception as e: print('FAIL:',e); sys.exit(2)
