import json, subprocess, sys
def probe(path):
    return json.loads(subprocess.check_output(['ffprobe','-v','error','-show_streams','-show_chapters','-show_format','-of','json',path]))
def check(source,target):
    a,b=probe(source),probe(target)
    v=[s for s in b['streams'] if s['codec_type']=='video']
    au=[s for s in b['streams'] if s['codec_type']=='audio']
    assert len(v)==1 and v[0]['codec_name']=='h264' and (v[0]['width'],v[0]['height'])==(1080,1920)
    assert len(au)==1 and au[0]['codec_name']=='aac'
    assert len(b['chapters'])==8
    assert [(c['start_time'],c['end_time'],c['tags']['title']) for c in a['chapters']]==[(c['start_time'],c['end_time'],c['tags']['title']) for c in b['chapters']]
    assert abs(float(a['format']['duration'])-float(b['format']['duration']))<0.1
    subprocess.run(['ffmpeg','-v','error','-xerror','-i',target,'-map','0:v:0','-map','0:a:0','-f','null','-'],check=True)
    print('PASS: 1080x1920 H264 AAC, 8 chapters unchanged, full AV decode')
if __name__=='__main__':check(*sys.argv[1:3])
