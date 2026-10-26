"""Synthetic only; no inherited or confidential media in CI."""
from pathlib import Path
import subprocess
import tempfile
from audio_caption_audit import read_energy,analyze,meter_png

with tempfile.TemporaryDirectory() as tmp:
    p=Path(tmp)/'tone.wav'
    subprocess.run(['ffmpeg','-v','error','-f','lavfi','-i',
        'sine=frequency=420:duration=2:sample_rate=16000','-y',str(p)],check=True)
    energy=read_energy(p)
    assert len(energy)>=59
    rows=analyze(energy,((0.1,1.8),))
    assert rows[0]['activity_ratio']>0.9
    img=Path(tmp)/'meter.png'
    meter_png(img,energy,15,((0.1,1.8),))
    assert img.stat().st_size>100
    print('Synthetic audio energy audit + visual meter: PASS')
