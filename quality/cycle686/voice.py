"""Offline Japanese TTS with measured scene-aligned SRT. REVIEW ONLY."""
from pathlib import Path
import json, shutil, subprocess, wave

GENRES = ('ai_productivity','trivia','cooking','beauty','finance','wellness','travel','product_demo','story','business')
LINES = (
 '四か月の合計は、六百五十。','毎月の集計、面倒ですよね。','AIに整理を頼みます。',
 '数字が表になります。','表計算に貼り付けます。','サム関数で検算します。',
 'グラフで比べます。','合計を確かめましょう。','手作業から、検算へ。','保存して試してね。'
)

def locate(patterns):
 for pat in patterns:
  for root in ('/usr/share','/var/lib'):
   matches=list(Path(root).glob(pat))
   if matches: return str(matches[0])
 raise RuntimeError('Japanese dictionary or voice model missing')

def wav_duration(path):
 with wave.open(str(path),'rb') as f: return f.getnframes()/f.getframerate()

def timestamp(seconds):
 ms=round(seconds*1000)
 return f'{ms//3600000:02}:{ms//60000%60:02}:{ms//1000%60:02},{ms%1000:03}'

def build(out, genre='ai_productivity'):
 if genre not in GENRES: raise ValueError('unsupported genre')
 exe=shutil.which('open_jtalk')
 if not exe: raise RuntimeError('Japanese TTS unavailable: no narration generated')
 dic=locate(('**/open-jtalk/naist-jdic','**/open_jtalk_dic_utf_8-*'))
 model=locate(('**/nitech_jp_atr503_m001.htsvoice','**/mei_normal.htsvoice'))
 out=Path(out);out.mkdir(parents=True,exist_ok=True)
 items=[]
 for i,line in enumerate(LINES):
  raw=out/f'raw_{i:02}.wav';seg=out/f'ja_{i:02}.wav'
  subprocess.run([exe,'-x',dic,'-m',model,'-r','1.55','-ow',str(raw)],input=line.encode('utf8'),check=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
  sec=wav_duration(raw)
  if sec<0.05: raise RuntimeError('empty speech')
  tempo=max(1.0,sec/1.75)
  if tempo>2.0: raise RuntimeError(f'speech too long in scene {i}')
  subprocess.run(['ffmpeg','-hide_banner','-loglevel','error','-y','-i',str(raw),'-af',f'atempo={tempo:.5f},aresample=48000','-ac','1',str(seg)],check=True)
  sec=wav_duration(seg)
  if sec>1.95: raise RuntimeError(f'speech scene {i} overflow: {sec}')
  items.append(dict(scene=i,text=line,start=i*2.0,end=i*2.0+sec,segment=str(seg)))
 args=[]
 for item in items: args+=['-i',item['segment']]
 chains=[f'[{i}:a]adelay={i*2000}[s{i}]' for i in range(len(items))]
 chains+=[''.join(f'[s{i}]' for i in range(len(items)))+f'amix=inputs={len(items)}:duration=longest:normalize=0,apad=pad_dur=20,atrim=0:20[a]']
 final=out/'narration_ja.wav'
 subprocess.run(['ffmpeg','-hide_banner','-loglevel','error','-y',*args,'-filter_complex',';'.join(chains),'-map','[a]','-ar','48000','-ac','1',str(final)],check=True)
 if abs(wav_duration(final)-20)>0.05: raise RuntimeError('narration not 20s')
 (out/'captions_ja.srt').write_text('\n'.join(f"{r['scene']+1}\n{timestamp(r['start'])} --> {timestamp(r['end'])}\n{r['text']}\n" for r in items),encoding='utf8')
 (out/'timings_ja.json').write_text(json.dumps(items,ensure_ascii=False,indent=2),encoding='utf8')
 return final

if __name__=='__main__':
 import argparse
 p=argparse.ArgumentParser();p.add_argument('--out',required=True);p.add_argument('--genre',default='ai_productivity')
 a=p.parse_args();print(build(a.out,a.genre))
