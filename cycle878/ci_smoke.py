"""Free synthetic-only smoke: verifies FFmpeg actually renders Japanese caption filter."""
from pathlib import Path
import subprocess,tempfile
import shutil
from cycle878.caption_safe_area import CaptionCue,filter_graph,write_textfiles

def main():
    exe=shutil.which("ffmpeg")
    if not exe:raise RuntimeError("system FFmpeg with drawtext is required")
    with tempfile.TemporaryDirectory() as td:
        td=Path(td)
        src=td/'synthetic.mp4';out=td/'captioned.mp4'
        subprocess.run([exe,'-v','error','-f','lavfi','-i','color=c=0x112233:s=1080x1920:r=30:d=1',
                        '-f','lavfi','-i','sine=frequency=440:sample_rate=48000:duration=1',
                        '-shortest','-c:v','libx264','-preset','ultrafast','-pix_fmt','yuv420p',
                        '-c:a','aac',str(src)],check=True,timeout=60)
        cues=(CaptionCue(.1,.9,('作業の確認を始める。','結果を見て判断する。')),)
        write_textfiles(cues,td)
        subprocess.run([exe,'-v','error','-i',str(src),'-vf',filter_graph(cues,td),
                        '-c:v','libx264','-preset','ultrafast','-c:a','copy',str(out)],check=True,timeout=60)
        subprocess.run([exe,'-v','error','-xerror','-i',str(out),'-f','null','-'],check=True,timeout=60)
        assert out.stat().st_size>5000
        print('Synthetic Japanese caption A/V render and full decode PASS (not finished MP4)')

if __name__=='__main__':main()
