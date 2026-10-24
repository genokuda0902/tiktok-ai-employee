"""Generate original 9:16 CI slides and a synthetic BEEP (not Japanese speech)."""
import argparse,importlib.util,json,subprocess
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
def create(root:Path,genre='sales_business'):
 src=root/'source';src.mkdir(parents=True,exist_ok=True)
 base=Path(__file__).resolve().parents[1]/'cycle817'/'render817.py'
 spec=importlib.util.spec_from_file_location('r817',base)
 m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
 if genre not in m.GENRE_ACCENTS:raise ValueError('unknown genre')
 font=ImageFont.truetype('/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc',64)
 for i,parts in enumerate(m.PHRASES):
  im=Image.new('RGB',(1080,1920),(9,30+i*3,48+i*2));d=ImageDraw.Draw(im)
  d.rounded_rectangle((65,65,1015,180),radius=24,fill=m.GENRE_ACCENTS[genre])
  d.text((90,270),f'検証用 {i+1}/8',font=font,fill='white')
  d.text((90,450),''.join(parts)[:12],font=font,fill='white')
  for j in range(i+1):d.rounded_rectangle((90+j*106,700,175+j*106,850),radius=15,fill=m.GENRE_ACCENTS[genre])
  d.text((90,990),'合成素材・投稿不可',font=font,fill='white')
  im.save(src/f'scene_{i+1:02}.png')
 durations=[3.355,3.085,3.025,3.285,3.265,3.36,2.97,3.495]
 (src/'voice_timing.json').write_text(json.dumps({'sentences':[{'text':''.join(p),'seconds':t} for p,t in zip(m.PHRASES,durations)]},ensure_ascii=False))
 subprocess.run(['ffmpeg','-y','-hide_banner','-loglevel','error','-f','lavfi','-i','sine=frequency=440:sample_rate=48000:duration=25.833333','-af','volume=0.07','-c:a','aac','-b:a','128k',str(src/'voice.m4a')],check=True)
 (root/'NOT_FOR_PUBLICATION.txt').write_text('Synthetic beep, not Japanese narration. Review only.\n')
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--root',type=Path,required=True);p.add_argument('--genre',default='sales_business');a=p.parse_args();create(a.root,a.genre)
