"""Native Japanese Open JTalk QA only; never publish generated audio without review."""
from pathlib import Path
import subprocess,wave,json
LINES=('四か月の売上をまとめます。','数字は百二十、百五十、二百、百八十。','表に並べて、合計を確認。','合計は六百五十です。','整理して、最後に検算しましょう。')
def discover(roots=('/usr/share','/var/lib/mecab')):
    voices=[];dics=[]
    for root in roots:
        r=Path(root)
        if not r.exists(): continue
        voices.extend(r.rglob('*.htsvoice'))
        dics.extend(p.parent for p in r.rglob('sys.dic') if 'open-jtalk' in str(p).lower() or 'naist' in str(p).lower())
    if not voices or not dics: raise RuntimeError('Open JTalk Japanese dictionary or voice missing')
    return str(voices[0]),str(dics[0])
def synthesize(out_dir,voice=None,dictionary=None):
    voice,dictionary=(voice,dictionary) if voice and dictionary else discover()
    out=Path(out_dir);out.mkdir(parents=True,exist_ok=True);cursor=0.;timing=[]
    for i,line in enumerate(LINES):
        dest=out/f'ja_{i:02d}.wav'
        subprocess.run(['open_jtalk','-x',dictionary,'-m',voice,'-ow',str(dest)],input=line,encoding='utf-8',check=True,timeout=45)
        with wave.open(str(dest),'rb') as w:
            if w.getnframes()==0: raise RuntimeError('empty Japanese WAV')
            duration=w.getnframes()/w.getframerate()
        timing.append({'text':line,'start':round(cursor,3),'end':round(cursor+duration,3),'file':dest.name})
        cursor+=duration+0.15
    (out/'native_ja_timeline.json').write_text(json.dumps(timing,ensure_ascii=False,indent=2),encoding='utf-8')
    (out/'REVIEW_ONLY.txt').write_text('Pronunciation, license, subtitle alignment and publication are NOT approved.\n')
    return timing
if __name__=='__main__':
    import argparse
    p=argparse.ArgumentParser();p.add_argument('--out',default='output/cycle690-ja-voice');a=p.parse_args()
    print(json.dumps(synthesize(a.out),ensure_ascii=False,indent=2))
