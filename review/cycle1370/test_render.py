import json,subprocess
from render import CUES,stamp,OUTPUT
def test_timing():
 assert len(CUES)==4
 assert stamp(2.5)=='00:00:02,500'
def test_subtitle_track():
 assert OUTPUT.is_file()
 p=subprocess.run(['ffprobe','-v','error','-show_streams','-of','json',str(OUTPUT)],capture_output=True,text=True,check=True)
 streams=json.loads(p.stdout)['streams']
 assert any(s['codec_type']=='subtitle' and s['codec_name']=='mov_text' for s in streams)
 assert any(s['codec_type']=='audio' for s in streams)
 assert any(s['codec_type']=='video' and s['width']==1080 and s['height']==1920 for s in streams)
