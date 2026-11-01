"""Run an offline Japanese-text synthetic end-to-end encode/decode check."""
from __future__ import annotations
import json
import subprocess
import tempfile
from pathlib import Path
from caption_clarity import run

FONT = '/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc'

def execute():
    with tempfile.TemporaryDirectory() as td:
        td = Path(td)
        src, dst = td / 'synthetic.mp4', td / 'enhanced.mp4'
        subprocess.run(['ffmpeg','-hide_banner','-nostdin','-y','-loglevel','error',
                        '-f','lavfi','-i','color=c=0x071020:s=1080x1920:r=30:d=2',
                        '-f','lavfi','-i','sine=frequency=440:sample_rate=48000:duration=2',
                        '-vf',f"drawtext=fontfile={FONT}:text='日本語字幕の確認':fontcolor=white:fontsize=64:x=120:y=1460",
                        '-frames:v','60','-c:v','libx264','-preset','ultrafast','-crf','23',
                        '-c:a','aac','-metadata:s:a:0','language=jpn',str(src)],check=True)
        run(src,dst)
        info=json.loads(subprocess.check_output(['ffprobe','-v','error','-show_streams','-of','json',str(dst)]))
        video=next(s for s in info['streams'] if s['codec_type']=='video')
        audio=next(s for s in info['streams'] if s['codec_type']=='audio')
        assert (video['width'],video['height'],video['r_frame_rate'])==(1080,1920,'30/1')
        assert audio['codec_name']=='aac'
        subprocess.run(['ffmpeg','-v','error','-xerror','-i',str(dst),'-f','null','-'],check=True)
        print('SYNTHETIC_2S_JAPANESE_CAPTION_VIDEO_AUDIO_FULL_DECODE_PASS')

if __name__=='__main__':execute()
