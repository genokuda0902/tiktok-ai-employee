"""Synthetic 1080x1920 1.5-second test: no real user media in CI."""
import sys
import tempfile
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from focus_cue import render, run
with tempfile.TemporaryDirectory() as tmp:
    source, target = Path(tmp) / 'synthetic.mp4', Path(tmp) / 'out.mp4'
    run(['ffmpeg','-v','error','-y','-f','lavfi','-i','color=c=0x08151b:s=1080x1920:r=30:d=1.5',
         '-f','lavfi','-i','sine=frequency=440:sample_rate=48000:duration=1.5',
         '-c:v','libx264','-preset','ultrafast','-pix_fmt','yuv420p','-c:a','aac','-shortest',source])
    qa = render(source, target, 'ai', (510, 970, 180, 80), .3, 1.2)
    assert qa['frames'] == 45 and qa['aac_bitstream_identical'] and qa['full_av_decode'] == 'PASS'
    print('Synthetic 45-frame 1080x1920 A/V smoke PASS')
