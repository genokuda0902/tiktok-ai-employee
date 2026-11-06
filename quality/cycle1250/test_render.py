import json,subprocess
from render import render
def test_render(tmp_path):
    p=render(tmp_path/'demo.mp4')
    assert p.exists() and p.stat().st_size>10000
    info=json.loads(subprocess.check_output(['ffprobe','-v','error','-show_streams','-show_format','-of','json',str(p)]))
    v=next(s for s in info['streams'] if s['codec_type']=='video')
    assert (v['width'],v['height'])==(720,1280)
    assert 11.9<float(info['format']['duration'])<12.1
    subprocess.run(['ffmpeg','-v','error','-i',str(p),'-f','null','-'],check=True)
