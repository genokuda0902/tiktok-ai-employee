"""Cycle442: zero-cost reusable kinetic overlays for 10 genres.
Needs: Pillow, ffmpeg, a rights-cleared 1080x1920 input with AAC audio.
Audio is preserved as SFX; Japanese narration is NOT generated here.
"""
import os,subprocess,json,hashlib
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
ROOT=Path(__file__).resolve().parent
SOURCE=Path(os.getenv("CYCLE442_SOURCE_MP4","/mnt/data/tiktok_cycle441_subscription_SOUND_DESIGN_REVIEW_ONLY_916.mp4"))
OUTPUT=Path(os.getenv("CYCLE442_OUTPUT_MP4","/mnt/data/tiktok_cycle442_subscription_KINETIC_REVIEW_ONLY_916.mp4"))
FONT=os.getenv("CYCLE442_JA_FONT","/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc")
GENRES=['AI・仕事効率化','美容・身だしなみ','恋愛・心理','お金・節約','営業・ビジネス','転職・キャリア','健康・生活改善','雑学・科学','旅行・グルメ','商品比較・暮らし']
CHIPS=[(.08,1.42,'見落としがちな固定費'),(4.12,6.62,'月額だけで判断しない'),(17.58,19.82,'まず明細を確認')]
def run(cmd):
 p=subprocess.run(cmd,capture_output=True,text=True)
 if p.returncode:raise RuntimeError(p.stderr[-1200:])
 return p.stdout
def make_chip(text,i):
 im=Image.new('RGBA',(850,104),(0,0,0,0));d=ImageDraw.Draw(im)
 d.rounded_rectangle((4,4,846,100),radius=29,fill=(8,38,55,240),outline=(103,223,189,240),width=3)
 d.rounded_rectangle((18,22,36,82),radius=9,fill=(103,223,189,255))
 d.text((65,19),text,font=ImageFont.truetype(FONT,42),fill=(248,250,247,255))
 path=ROOT/f'chip_{i:02d}.png';im.save(path);return path
def main():
 if not SOURCE.is_file():raise FileNotFoundError('Input MP4 required: '+str(SOURCE))
 OUTPUT.parent.mkdir(parents=True,exist_ok=True)
 pngs=[make_chip(c[2],i) for i,c in enumerate(CHIPS)]
 args=['-i',str(SOURCE)]
 for p in pngs:args+=['-loop','1','-framerate','30','-i',str(p)]
 filters=[];prev='0:v'
 for i,(start,end,_) in enumerate(CHIPS,1):
  x=f"if(lt(t,{start+.45:.2f}),-850+2045*(t-{start:.2f}),70)"
  filters.append(f"[{prev}][{i}:v]overlay=x='{x}':y=154:enable='between(t,{start:.2f},{end:.2f})':shortest=1:format=auto[v{i}]")
  prev=f'v{i}'
 run(['ffmpeg','-y','-v','error',*args,'-filter_complex',';'.join(filters),'-map',f'[{prev}]','-map','0:a:0','-c:v','libx264','-preset','veryfast','-crf','20','-pix_fmt','yuv420p','-r','30','-c:a','copy','-t','20','-movflags','+faststart',str(OUTPUT)])
 q=json.loads(run(['ffprobe','-v','error','-show_entries','stream=codec_name,codec_type,width,height,nb_frames:format=duration','-of','json',str(OUTPUT)]))
 v=next(s for s in q['streams'] if s['codec_type']=='video');a=next(s for s in q['streams'] if s['codec_type']=='audio')
 assert (v['codec_name'],v['width'],v['height'],v['nb_frames'])==('h264',1080,1920,'600')
 assert a['codec_name']=='aac'
 for s in ['0:v:0','0:a:0']:run(['ffmpeg','-v','error','-xerror','-i',str(OUTPUT),'-map',s,'-f','null','-'])
 manifest={'cycle':442,'previous_cycle':441,'genres_configured':GENRES,'cost_jpy':0,'output_sha256':hashlib.sha256(OUTPUT.read_bytes()).hexdigest(),'japanese_voice':'MISSING','voice_subtitle_sync':'NOT_VERIFIED','approval':'HUMAN_REVIEW / PUBLICATION_NOT_APPROVED'}
 (ROOT/'manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2),encoding='utf-8')
if __name__=='__main__':main()
