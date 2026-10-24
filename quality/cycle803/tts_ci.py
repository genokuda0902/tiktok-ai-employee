#!/usr/bin/env python3
"""Free Japanese Open JTalk voice generation for cycle803; review-only."""
import json, subprocess, wave
from pathlib import Path
ROOT=Path(__file__).resolve().parent
OUT=ROOT/'out'
OUT.mkdir(parents=True,exist_ok=True)
SENTENCES=[
    '仕事ができる人は、質問が違う。',
    'まず、目指すゴールを確認する。',
    '次に、今の数字を確かめる。',
    'そして、理想との差を一つに絞る。',
    '原因には、なぜを三回重ねる。',
    '対策は、今日できる行動に変える。',
    '結果を見て、また修正する。',
    '小さな改善が、強いチームをつくる。',
]
GENRES=['ai_work','beauty','love_psychology','money_saving','sales_business','career','health_life','science','travel_food','product_life']
def find_resources():
    voices=list(Path('/usr/share').rglob('*.htsvoice'))
    dictionaries=list(Path('/var/lib/mecab/dic').rglob('naist-jdic'))
    if not voices or not dictionaries: raise RuntimeError('Open JTalk voice or dictionary unavailable')
    return str(dictionaries[0]),str(voices[0])
def main():
    dic,model=find_resources()
    segments=[]
    for i,s in enumerate(SENTENCES):
        output=OUT/f'speech_{i:02d}.wav'
        subprocess.run(['open_jtalk','-x',dic,'-m',model,'-r','1.07','-ow',str(output)],input=s.encode('utf-8'),check=True)
        with wave.open(str(output),'rb') as w:
            duration=w.getnframes()/w.getframerate()
            assert w.getnchannels()==1 and 0.4<duration<12
            info={'sample_rate':w.getframerate(),'channels':w.getnchannels()}
        segments.append({'scene':i+1,'text':s,'seconds':duration,'filename':output.name})
    manifest=OUT/'audio_concat.txt'
    manifest.write_text(''.join(f"file '{(OUT/s['filename']).resolve()}'\n" for s in segments))
    output=OUT/'cycle803_business_japanese.m4a'
    subprocess.run(['ffmpeg','-hide_banner','-loglevel','error','-y','-f','concat','-safe','0','-i',str(manifest),'-ar','48000','-ac','1','-c:a','aac','-b:a','128k',str(output)],check=True)
    metadata={'cycle':803,'genre':'sales_business','sentences':segments,'voice_engine':'Open JTalk','voice_model':Path(model).name,'voice_info':info,'rights_review_required':True,'status':'HUMAN_REVIEW / PUBLICATION_NOT_APPROVED','ten_genres':GENRES}
    (OUT/'voice_timing.json').write_text(json.dumps(metadata,ensure_ascii=False,indent=2))
    subprocess.run(['ffmpeg','-v','error','-xerror','-i',str(output),'-f','null','-'],check=True)
    print('NEW Japanese voice generated',output,'seconds',round(sum(s['seconds'] for s in segments),3))
if __name__=='__main__':main()
