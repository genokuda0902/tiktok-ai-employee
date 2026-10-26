"""Public synthetic-only CI smoke; never fetches or uploads private narration."""
import json, subprocess, tempfile
import imageio_ffmpeg
from pathlib import Path
from kinetic_endcard import DEFAULT, GENRES, stage_progress, validate_story
for genre in GENRES:
    from dataclasses import replace
    assert validate_story(replace(DEFAULT,genre=genre))
assert stage_progress(102)[1]==1
ffmpeg=imageio_ffmpeg.get_ffmpeg_exe()
with tempfile.TemporaryDirectory() as td:
    out=Path(td)/'synthetic.mp4'
    subprocess.run([ffmpeg,'-v','error','-y','-f','lavfi','-i','color=c=navy:s=360x640:r=30:d=1',
                    '-f','lavfi','-i','sine=frequency=440:sample_rate=48000:duration=1',
                    '-c:v','libx264','-pix_fmt','yuv420p','-c:a','aac','-shortest',str(out)],check=True,timeout=90)
    result=subprocess.run([ffmpeg,'-v','error','-i',str(out),'-f','null','-'],capture_output=True,timeout=90)
    assert result.returncode==0
print('CI synthetic A/V decode + 10 genre end-card copy PASS')
