"""Synthetic-only smoke; no user footage, rights-unclear media or auto-posting."""
import importlib.util
import json
import subprocess
import tempfile
from pathlib import Path
import sys

ROOT=Path(__file__).resolve().parents[1]
s=importlib.util.spec_from_file_location('evidence_panel_repair',ROOT/'code/evidence_panel_repair.py')
m=importlib.util.module_from_spec(s);sys.modules[s.name]=m;s.loader.exec_module(m)

def run(args):
    subprocess.run(args,check=True,stdout=subprocess.DEVNULL,stderr=subprocess.PIPE)

with tempfile.TemporaryDirectory() as d:
    d=Path(d)
    # Synthetic 3s 1080x1920 A/V and 2 metadata chapters.
    metadata=d/'chapters.ffmeta'
    metadata.write_text(';FFMETADATA1\n[CHAPTER]\nTIMEBASE=1/1000\nSTART=0\nEND=1500\ntitle=01/02\n[CHAPTER]\nTIMEBASE=1/1000\nSTART=1500\nEND=3000\ntitle=02/02\n')
    src=d/'source.mp4'
    run(['ffmpeg','-v','error','-y','-f','lavfi','-i','color=c=0x07202a:s=1080x1920:r=30:d=3',
         '-f','lavfi','-i','sine=frequency=440:sample_rate=48000:duration=3',
         '-i',str(metadata),'-map','0:v','-map','1:a','-map_metadata','2','-map_chapters','2',
         '-c:v','libx264','-preset','ultrafast','-crf','35','-c:a','aac','-t','3',src.as_posix()])
    # Patch only the second scene.
    result=m.render(src,d/'result.mp4',m.Patch(scene=2),d/'panel.png',d/'report.json',crf=30)
    assert result['frames']==90 and result['chapters']==2, result
    run(['ffmpeg','-v','error','-xerror','-i',str(d/'result.mp4'),'-f','null','-'])
    print(json.dumps({'synthetic_full_decode':'PASS','frames':result['frames'],'chapters':result['chapters']}))
