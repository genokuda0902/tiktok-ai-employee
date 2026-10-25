"""cycle831 editorial image-slide renderer; no posting, paid APIs or user data.
The optional AI-generated 8-panel storyboard is a LOCAL REVIEW ASSET and is not
committed. CI uses the original procedural scene images as a documented fallback.
"""
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont,ImageEnhance
import argparse,json,subprocess,hashlib,math
W,H=1080,1920
FRAMES=[101,93,91,99,98,101,89,103]
COLORS={'sales_business':'#FFB85C','ai_work':'#43D8CC','beauty':'#E3A1B8','love_psychology':'#E2A2C1','money_saving':'#B7A05C','career':'#6288CF','health_life':'#78B78C','science':'#D39D69','travel_food':'#947CD0','product_life':'#65AABF'}
HEAD=['AIで仕事を早くする','繰り返す作業を探す','完成見本を用意する','目的と条件を伝える','AIの回答を確認する','修正点は一つずつ','良い指示を保存する','小さな時短を習慣に']
SUB=['最初の一歩を決めよう','毎日の仕事を見直す','ゴールを具体的にする','伝える内容を整理する','数字・日付・根拠を見る','差分を言葉にする','次から迷わない仕組み','まずは今日、ひとつ']
ACT=['仕事を3つに分ける','毎日の作業を1つ選ぶ','完成例を1つ用意','目的・条件・見本を書く','数字と根拠を確認','直す点を1つだけ伝える','指示文を保存する','明日も1回試す']
FONT='/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc'
def ft(n):return ImageFont.truetype(FONT,n)
def rgb(h):return tuple(int(h[i:i+2],16) for i in (1,3,5))
def cover(im,w,h):
    sc=max(w/im.width,h/im.height); im=im.resize((math.ceil(im.width*sc),math.ceil(im.height*sc)),Image.Resampling.LANCZOS)
    x=(im.width-w)//2;y=(im.height-h)//2
    return im.crop((x,y,x+w,y+h))
def storyboard_panel(path,i):
    im=Image.open(path).convert('RGB');w,h=im.size
    if w<1100 or h<1100:raise ValueError('Expected original eight-panel image')
    cw=w/4;x0=int((i%4)*cw+cw*.055);x1=int((i%4+1)*cw-cw*.055)
    if i==4:x1=int((i%4)*cw+cw*.55)
    return im.crop((x0,int(h*(.155 if i<4 else .595)),x1,int(h*(.400 if i<4 else .815))))
# cycle832: enlarge the storytelling image and reserve the caption safe area.
# Image box: 972x1030 (was 684x910); no tiny secondary sidebar.
PHOTO_BOX=(54,390,1026,1420)
CAPTION_SAFE_TOP=1450
def slide(i,art,dest,genre='ai_work'):
    if genre not in COLORS:raise ValueError('unknown genre')
    if not 0<=i<len(HEAD):raise ValueError('scene index')
    accent=rgb(COLORS[genre])
    im=Image.new('RGB',(W,H),(7,24,35))
    d=ImageDraw.Draw(im)
    for y in range(H):
        t=y/H
        d.line((0,y,W,y),fill=(int(6+3*t),int(21+10*t),int(34+10*t)))
    d.rounded_rectangle((54,55,370,120),radius=30,fill=(20,67,72))
    d.text((82,70),'AI WORK / 08',font=ft(29),fill='white')
    d.text((830,70),f'{i+1:02d} / 08',font=ft(38),fill=accent)
    d.text((54,186),HEAD[i],font=ft(65),fill=(247,249,249))
    d.text((57,296),SUB[i],font=ft(37),fill=(179,218,218))
    x0,y0,x1,y1=PHOTO_BOX
    w,h=x1-x0,y1-y0
    photo=ImageEnhance.Contrast(cover(art,w,h)).enhance(1.07)
    mask=Image.new('L',(w,h))
    ImageDraw.Draw(mask).rounded_rectangle((0,0,w-1,h-1),radius=28,fill=255)
    im.paste(photo,(x0,y0),mask)
    # Dark gradient belongs inside the image, not in the Japanese subtitle zone.
    shade=Image.new('RGBA',(w,h),(0,0,0,0))
    sh=ImageDraw.Draw(shade)
    for yy in range(h-310,h):
        alpha=int(195*(yy-(h-310))/310)
        sh.line((0,yy,w,yy),fill=(3,17,26,alpha))
    im.paste(Image.alpha_composite(im.crop(PHOTO_BOX).convert('RGBA'),shade).convert('RGB'),(x0,y0),mask)
    d=ImageDraw.Draw(im)
    d.rounded_rectangle((80,1240,1000,1380),radius=23,fill=(7,31,43),outline=accent,width=3)
    d.ellipse((110,1290,140,1320),fill=accent)
    d.text((165,1276),ACT[i],font=ft(43),fill='white')
    # Explicit bottom-caption-only region; never place CTA below PHOTO_BOX.
    d.rounded_rectangle((54,CAPTION_SAFE_TOP,1026,1808),radius=25,fill=(5,29,41),outline=(34,77,83),width=2)
    d.line((56,1840,1024,1840),fill=(46,93,99),width=2)
    dest=Path(dest);dest.parent.mkdir(parents=True,exist_ok=True)
    im.save(dest,optimize=True)
def make_slides(root,collage=None,genre='ai_work'):
    root=Path(root);source=root/'source'
    # Load all sources before overwriting, including CI fallback art.
    arts=[storyboard_panel(collage,i) if collage else Image.open(source/f'scene_{i+1:02}.png').convert('RGB').copy() for i in range(8)]
    for i,art in enumerate(arts):slide(i,art,source/f'scene_{i+1:02}.png',genre)
    (source/'asset_provenance831.json').write_text(json.dumps({'origin':'AI-generated storyboard' if collage else 'original procedural CI fallback','publication_approved':False,'rights_review_required':True}))
def cmd(xs):subprocess.run(xs,check=True)
def make_video(root):
    root=Path(root);out=root/'output';out.mkdir(exist_ok=True)
    cap=(out/'captions828.ass').read_text(encoding='utf-8')
    cap=cap.replace(r'\pos(540,1530)',r'\pos(540,1640)')
    (out/'captions831.ass').write_text(cap,encoding='utf-8')
    if cap.count('Dialogue: 0,')!=24:raise RuntimeError('subtitle states missing')
    ins=[];parts=[]
    for i,n in enumerate(FRAMES):
        ins+=['-i',str(root/'source'/f'scene_{i+1:02}.png')]
        direction=f'(iw-iw/zoom)*on/{n}' if i%2==0 else f'(iw-iw/zoom)*(1-on/{n})'
        parts.append(f"[{i}:v]zoompan=z='min(1.0+on*0.00024,1.025)':x='{direction}':y='(ih-ih/zoom)/2':d={n}:s=1080x1920:fps=30,setsar=1,format=yuv420p[v{i}]")
    parts.append(''.join(f'[v{i}]' for i in range(8))+'concat=n=8:v=1:a=0[vcat]')
    parts.append(f'[vcat]ass={out/"captions831.ass"}:fontsdir=/usr/share/fonts/opentype/noto[vout]')
    target=out/'cycle831_PHOTO_EDITORIAL_JAPANESE_HUMAN_REVIEW.mp4'
    cmd(['ffmpeg','-hide_banner','-loglevel','error','-y',*ins,'-i',str(root/'source'/'voice_mastered828.m4a'),'-filter_complex',';'.join(parts),'-map','[vout]','-map','8:a:0','-c:v','libx264','-preset','veryfast','-crf','23','-pix_fmt','yuv420p','-r','30','-c:a','aac','-b:a','160k','-ar','48000','-af','apad','-t',str(sum(FRAMES)/30),'-movflags','+faststart',str(target)])
    return target
def verify(root):
    root=Path(root);target=root/'output'/'cycle831_PHOTO_EDITORIAL_JAPANESE_HUMAN_REVIEW.mp4'
    info=json.loads(subprocess.check_output(['ffprobe','-v','error','-show_streams','-show_format','-of','json',str(target)]))
    v=next(s for s in info['streams'] if s['codec_type']=='video');a=next(s for s in info['streams'] if s['codec_type']=='audio')
    decoded=subprocess.run(['ffmpeg','-v','error','-xerror','-i',str(target),'-f','null','-'],capture_output=True)
    checks={'1080x1920':(v['width'],v['height'])==(1080,1920),'h264_30fps':v['codec_name']=='h264' and v['r_frame_rate']=='30/1','775_frames':int(v['nb_frames'])==775,'aac_48khz':a['codec_name']=='aac' and a['sample_rate']=='48000','full_decode':decoded.returncode==0,'24_captions':(root/'output'/'captions831.ass').read_text().count('Dialogue: 0,')==24,'ten_genres':len(COLORS)==10}
    report={'cycle':831,'checks':checks,'passed':sum(checks.values()),'total':len(checks),'sha256':hashlib.sha256(target.read_bytes()).hexdigest(),'source':'procedural fallback' if not (root/'source'/'generated_art_marker').exists() else 'AI generated','status':'HUMAN_REVIEW / PUBLICATION_NOT_APPROVED','visual_parity_with_local':False}
    (root/'output'/'qa831.json').write_text(json.dumps(report,ensure_ascii=False,indent=2))
    if not all(checks.values()):raise RuntimeError(str(checks))
    return report
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--root',required=True);p.add_argument('--step',choices=['slides','render','verify'],required=True);p.add_argument('--collage');p.add_argument('--genre',default='ai_work')
    a=p.parse_args()
    if a.step=='slides':make_slides(a.root,a.collage,a.genre)
    elif a.step=='render':print(make_video(a.root))
    else:print(json.dumps(verify(a.root),ensure_ascii=False,indent=2))
