#!/usr/bin/env python3
"""Rights-safe 4-second CI fixture with Open JTalk Japanese speech; not a production video."""
import argparse,json,subprocess
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
from first_second_comparison import run, FONT
W,H=1080,1920
def call(args):subprocess.run(args,check=True)
def create_fixture(out_dir,voice,dic):
    p=Path(out_dir);p.mkdir(parents=True,exist_ok=True)
    f=ImageFont.truetype(FONT,70);sm=ImageFont.truetype(FONT,40)
    base=Image.new('RGB',(W,H),'#0b1f35');d=ImageDraw.Draw(base)
    d.text((120,420),'AIで、集計を見直す',font=f,fill='white')
    d.text((120,570),'架空データの検証用映像',font=sm,fill='#91e8e5')
    d.text((120,850),'その集計、まだ手作業？',font=sm,fill='white')
    base.save(p/'base.png')
    for name,col,title in [('before',(78,98,110),'BEFORE'),('after',(25,122,132),'AFTER')]:
        im=Image.new('RGB',(W,H),col);dd=ImageDraw.Draw(im)
        dd.rounded_rectangle((100,400,980,1350),radius=60,outline='#d0f7f7',width=18)
        dd.text((180,700),title,font=f,fill='white')
        im.save(p/(name+'.png'))
    (p/'voice.txt').write_text('その集計、まだ手作業ですか。AIで整理します。\n',encoding='utf-8')
    call(['open_jtalk','-x',str(dic),'-m',str(voice),'-ow',str(p/'speech.wav'),str(p/'voice.txt')])
    call(['ffmpeg','-hide_banner','-loglevel','error','-y','-loop','1','-framerate','30','-t','4','-i',str(p/'base.png'),'-i',str(p/'speech.wav'),'-filter_complex','[1:a]apad,atrim=duration=4[a]','-map','0:v:0','-map','[a]','-c:v','libx264','-preset','veryfast','-crf','22','-pix_fmt','yuv420p','-c:a','aac','-b:a','128k','-movflags','+faststart',str(p/'base.mp4')])
    cfg={'canvas':[W,H],'mode':'review_only','hook_seconds':1.5,'headline':'その集計、\nまだ手作業？','subtitle':'BEFORE → AFTER を先に見せる','before_label':'BEFORE','after_label':'AFTER','before_crop':[0,0,W,H],'after_crop':[0,0,W,H],'disclosure':'※架空データによるCI検証映像','rights_reviewed':False,'publication_approved':False}
    return run(p/'base.mp4',p/'before.png',p/'after.png',p/'cycle788_ci_fixture.mp4',cfg,p/'report.json')
if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--out',required=True);ap.add_argument('--voice',required=True);ap.add_argument('--dic',required=True)
    a=ap.parse_args();print(json.dumps(create_fixture(a.out,a.voice,a.dic),ensure_ascii=False))
