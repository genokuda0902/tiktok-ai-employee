"""Offline Japanese narration for original-image GitHub CI review artifact.
NIT ATR503 M001 voice: CC BY 3.0, attribution bundled with artifact.
"""
import argparse, json, subprocess, wave
from pathlib import Path

DIC=Path('/var/lib/mecab/dic/open-jtalk/naist-jdic')
VOICE=Path('/usr/share/hts-voice/nitech-jp-atr503-m001/nitech_jp_atr503_m001.htsvoice')
CREDIT="""HUMAN REVIEW ONLY / NOT APPROVED FOR PUBLICATION
Japanese narration: Open JTalk / NIT ATR503 M001 HTS voice.
Copyright (c) 2003-2012 Nagoya Institute of Technology and
(c) 2003-2008 Tokyo Institute of Technology. CC BY 3.0.
https://sourceforge.net/projects/open-jtalk/files/HTS%20voice/hts_voice_nitech_jp_atr503_m001-1.05/
Visuals: original Pillow-generated synthetic graphics; no portraits.
No employee approval or TikTok upload.
"""
def run(*cmd,input_text=None):
    return subprocess.run(cmd,input=input_text,
      text=input_text is not None,check=True,capture_output=True)
def wav_duration(path):
    with wave.open(str(path),'rb') as f:
        return f.getnframes()/f.getframerate()
def atempo_chain(speed):
    if speed<1:raise ValueError('invalid speed')
    parts=[]
    while speed>2:
        parts.append('atempo=2.0');speed/=2
    parts.append(f'atempo={speed:.7f}')
    return ','.join(parts)
def generate(root):
    if not DIC.is_dir() or not VOICE.is_file():
        raise FileNotFoundError('Open JTalk voice/dictionary missing')
    src=root/'source'; temp=root/'_tts';temp.mkdir(parents=True,exist_ok=True)
    scenes=json.loads((src/'voice_timing.json').read_text(encoding='utf8'))['sentences']
    if len(scenes)!=8:raise ValueError('expected eight scenes')
    concat=[];speeds=[]
    for i,scene in enumerate(scenes):
        target=float(scene['seconds'])
        if target<=0.3 or not scene['text']:raise ValueError('invalid scene')
        raw=temp/f'raw_{i:02}.wav';fixed=temp/f'fixed_{i:02}.wav'
        run('open_jtalk','-x',str(DIC),'-m',str(VOICE),
            '-s','48000','-ow',str(raw),input_text=scene['text']+'\n')
        original=wav_duration(raw)
        speed=max(1.0,original/(target-0.16))
        speeds.append(round(speed,3))
        filt=atempo_chain(speed)+f',apad,atrim=duration={target:.6f},asetpts=N/SR/TB'
        run('ffmpeg','-y','-v','error','-i',str(raw),
            '-af',filt,'-ac','1','-ar','48000',str(fixed))
        if abs(wav_duration(fixed)-target)>0.002:raise RuntimeError('audio mismatch')
        concat.append(f"file '{fixed.resolve()}'")
    listing=temp/'concat.txt';listing.write_text('\n'.join(concat)+'\n')
    run('ffmpeg','-y','-v','error','-f','concat','-safe','0','-i',
        str(listing),'-c:a','aac','-b:a','160k',str(src/'voice.m4a'))
    (root/'VOICE_LICENSE_ATTRIBUTION.txt').write_text(CREDIT)
    (root/'NOT_FOR_PUBLICATION.txt').write_text('Review only.\n')
    (root/'tts_qa819.json').write_text(json.dumps({
        'language':'Japanese','engine':'Open JTalk','voice':'NIT ATR503 M001',
        'license':'CC BY 3.0','scene_speed_factors':speeds,
        'warning':'Speech naturalness and timing require human review'},
        ensure_ascii=False,indent=2))
    return src/'voice.m4a'
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--root',type=Path,required=True)
    print(generate(p.parse_args().root))
