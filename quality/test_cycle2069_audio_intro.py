from quality.cycle2069_audio_intro import build
from pathlib import Path
import subprocess

def test_build_command(monkeypatch):
    calls=[]
    monkeypatch.setattr(subprocess,"run",lambda cmd,check: calls.append((cmd,check)))
    build(Path("in.mp4"),Path("out.mp4"))
    cmd,check=calls[0]
    assert check and "afade=t=in:st=0:d=0.30" in cmd
    assert cmd[cmd.index("-c:v")+1]=="copy"
