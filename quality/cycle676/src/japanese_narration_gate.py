"""Offline Japanese speech quality gate. Requires local Open JTalk models."""
import argparse
import json
import shutil
import subprocess
import wave
from pathlib import Path

def synthesize(text, out, dictionary, voice, executable='open_jtalk'):
    if not shutil.which(executable):
        raise RuntimeError('Open JTalk missing; Japanese narration is NOT generated')
    if not Path(dictionary).is_dir() or not Path(voice).is_file():
        raise RuntimeError('Open JTalk dictionary or voice model missing')
    out=Path(out)
    out.parent.mkdir(parents=True,exist_ok=True)
    subprocess.run([executable,'-x',str(dictionary),'-m',str(voice),'-ow',str(out)],
                   input=text,encoding='utf8',check=True,stderr=subprocess.PIPE)
    with wave.open(str(out),'rb') as w:
        seconds=w.getnframes()/w.getframerate()
        frames=w.readframes(w.getnframes())
    if seconds < 0.1 or not any(x != 0 for x in frames):
        raise RuntimeError('Japanese speech WAV is silent or too short')
    return {'duration_seconds':round(seconds,3),'wav_path':str(out),'spoken_text':text,'speech_generated':True}

if __name__=='__main__':
    p=argparse.ArgumentParser()
    p.add_argument('--text',required=True)
    p.add_argument('--wav',required=True)
    p.add_argument('--dictionary',required=True)
    p.add_argument('--voice',required=True)
    args=p.parse_args()
    print(json.dumps(synthesize(args.text,args.wav,args.dictionary,args.voice),ensure_ascii=False))
