from PIL import Image, ImageDraw, ImageFont
from pathlib import Path
import subprocess, json, math, wave, struct

P = Path(__file__).resolve().parent
FONT = '/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc'
TITLE = ImageFont.truetype(FONT, 65)
BODY = ImageFont.truetype(FONT, 43)
SMALL = ImageFont.truetype(FONT, 34)
SCENES = [
    ('合計、まだ電卓で計算？', '3つの売上を一瞬で合計'),
    ('SUM関数を入力', 'セルに =SUM(B2:B4)'),
    ('数字を必ず確認', '元データと結果を照合'),
]

def render():
    for i, (head, sub) in enumerate(SCENES):
        im = Image.new('RGB', (1080, 1920), (9, 20, 38))
        d = ImageDraw.Draw(im)
        d.rounded_rectangle((62, 220, 1018, 1450), radius=35, fill=(23, 44, 68))
        d.rounded_rectangle((90, 265, 990, 390), radius=20, fill=(21, 104, 126))
        d.text((115, 282), f'STEP {i+1} / 3', font=TITLE, fill='white')
        d.text((90, 465), head, font=TITLE, fill='white')
        d.text((90, 585), sub, font=BODY, fill=(194, 235, 244))
        d.rounded_rectangle((90, 790, 990, 1280), radius=22, fill=(244, 248, 252))
        for row in range(5):
            d.line((120, 860 + row*75, 960, 860 + row*75), fill=(192, 205, 213), width=2)
        d.text((145, 900), ['1,200   3,400   2,100', '=SUM(B2:B4)', '1,200 + 3,400 + 2,100'][i], font=BODY, fill=(19, 45, 66))
        d.text((145, 1060), ['合計を出したい', 'Enterで計算', '合計：6,700'][i], font=BODY, fill=(10, 107, 123))
        d.rounded_rectangle((90, 1510, 990, 1630), radius=18, fill=(9, 40, 59))
        d.text((115, 1540), sub, font=SMALL, fill='white')
        d.rounded_rectangle((90, 1680, 990, 1698), radius=9, fill=(60, 78, 92))
        d.rounded_rectangle((90, 1680, 90 + 300*(i+1), 1698), radius=9, fill=(33, 210, 190))
        d.text((90, 1750), 'REVIEW ONLY / 公開未承認', font=SMALL, fill=(175, 190, 202))
        im.save(P / f'scene{i}.png')
    (P/'frames.txt').write_text(''.join(f"file 'scene{i}.png'\nduration 5\n" for i in range(3)) + "file 'scene2.png'\n", encoding='utf-8')
    rate = 24000
    with wave.open(str(P/'cue.wav'), 'wb') as f:
        f.setnchannels(1); f.setsampwidth(2); f.setframerate(rate)
        for n in range(15*rate):
            t=n/rate; local=t%5
            env=max(0, 1-local/0.22) if local<0.22 else 0
            f.writeframesraw(struct.pack('<h', int(1800*env*math.sin(2*math.pi*660*t))))
    subprocess.run(['ffmpeg','-y','-loglevel','error','-f','concat','-safe','0','-i',str(P/'frames.txt'),'-i',str(P/'cue.wav'),'-vf','fps=25,format=yuv420p','-c:v','libx264','-preset','ultrafast','-crf','27','-c:a','aac','-b:a','96k','-t','15','-movflags','+faststart',str(P/'cycle1427_REVIEW_ONLY.mp4')], check=True)
    (P/'captions.srt').write_text('1\n00:00:00,000 --> 00:00:05,000\n合計、まだ電卓で計算？\n\n2\n00:00:05,000 --> 00:00:10,000\nセルに =SUM(B2:B4)\n\n3\n00:00:10,000 --> 00:00:15,000\n元データと結果を照合\n', encoding='utf-8')
    (P/'qa.json').write_text(json.dumps({'japanese_narration':False,'audio':'original synthesized cue only','speech_synced_captions':False,'publication_approved':False,'scene_count':3},ensure_ascii=False,indent=2), encoding='utf-8')

if __name__ == '__main__':
    render()
