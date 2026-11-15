"""Synthetic review renderer. Never publish without narration, approvals and human review."""
import argparse, json, subprocess
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
SCENES=[('毎日の集計、まだ手作業？','課題を見つける'),('表を整理する','入力 → 集計 → 確認'),('数字の変化を見える化','架空データ：12 → 24'),('最後は人がチェック','AIの結果は必ず確認')]
FONT='/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc'
def render(out):
    out.mkdir(parents=True,exist_ok=True)
    font=ImageFont.truetype(FONT,62); small=ImageFont.truetype(FONT,39)
    for i,(headline,sub) in enumerate(SCENES):
        im=Image.new('RGB',(720,1280),(10,20,38)); d=ImageDraw.Draw(im)
        d.rounded_rectangle((48,180,672,1060),radius=30,fill=(26,43,65))
        d.rectangle((48,180,62,1060),fill=(52,210,197))
        d.text((85,295),f'0{i+1} / 04',font=small,fill=(75,220,202))
        d.text((85,465),headline,font=font,fill='white')
        d.text((85,645),sub,font=small,fill=(215,225,237))
        d.rounded_rectangle((85,855,85+int(530*(i+1)/4),876),radius=9,fill=(75,220,202))
        d.text((85,1140),'架空データ / REVIEW ONLY',font=small,fill=(175,190,207))
        im.save(out/f'scene_{i}.png')
    srt=''.join(f'{i+1}\n00:00:{i*3:02},000 --> 00:00:{(i+1)*3:02},000\n{h}\n\n' for i,(h,_) in enumerate(SCENES))
    (out/'captions.srt').write_text(srt,encoding='utf-8')
    manifest={'publication_approved':False,'narration_present':False,'asset_origin':'synthetic','duration_seconds':12,'resolution':[720,1280],'scene_count':4}
    (out/'manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2),encoding='utf-8')
    clips=[]
    for i in range(4):
        clip=out/f'clip_{i}.mp4'; clips.append(clip)
        subprocess.run(['ffmpeg','-hide_banner','-loglevel','error','-y','-loop','1','-framerate','24','-i',str(out/f'scene_{i}.png'),'-t','3','-vf','format=yuv420p','-c:v','libx264','-preset','ultrafast',str(clip)],check=True)
    playlist=out/'concat.txt'; playlist.write_text(''.join(f"file '{p.resolve()}'\n" for p in clips))
    target=out/'cycle1482_REVIEW_ONLY.mp4'
    subprocess.run(['ffmpeg','-hide_banner','-loglevel','error','-y','-f','concat','-safe','0','-i',str(playlist),'-c','copy','-movflags','+faststart',str(target)],check=True)
    return target
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--out',type=Path,default=Path('output/cycle1482'));args=p.parse_args();print(render(args.out))
