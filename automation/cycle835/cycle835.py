"""cycle835: independently generated hero and split-screen hook, human review only."""
from __future__ import annotations
import hashlib, json, subprocess
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageEnhance, ImageFilter, ImageChops

W,H=1080,1920
FRAMES=(101,93,91,99,98,101,89,103)
PHOTO=(62,390,1018,1390)
GENRE_PRESETS={
 'ai_work':('#40DDCB','AIで仕事を早くする','迷う','最初の一歩'),
 'sales_business':('#F4B65C','営業で結果を出す','悩む','行動する'),
 'beauty':('#F4A8BC','美容習慣を整える','手探り','自分らしく'),
 'romance':('#EBA9CD','伝わる会話をする','すれ違い','伝わる'),
 'saving':('#E9C970','家計を見直す','なんとなく','見える化'),
 'career':('#96B9FF','仕事を成長させる','迷う','一歩進む'),
 'wellness':('#A6DDB5','生活を整える','あわただしい','少し余裕'),
 'science':('#E7B28B','身近な科学を知る','疑問','発見'),
 'travel_food':('#C0A9F8','旅を楽しむ','計画前','計画後'),
 'productivity':('#88DCE1','毎日を効率化する','やることだらけ','一つずつ')
}
FONT='/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc'

def font(size): return ImageFont.truetype(FONT,size)

def crop_cover(image, size, focal=(.5,.5)):
    """Crop to target without stretching faces."""
    w,h=size; ratio=max(w/image.width,h/image.height)
    rw,rh=round(image.width*ratio),round(image.height*ratio)
    im=image.resize((rw,rh),Image.Resampling.LANCZOS)
    left=max(0,min(rw-w,round(rw*focal[0]-w/2)))
    top=max(0,min(rh-h,round(rh*focal[1]-h/2)))
    return im.crop((left,top,left+w,top+h))

def draw_hook(slide, hero, second_slide, genre='ai_work'):
    if genre not in GENRE_PRESETS: raise ValueError(genre)
    accent,headline,before_label,after_label=GENRE_PRESETS[genre]
    canvas=slide.convert('RGB').copy()
    base=second_slide.crop(PHOTO).convert('RGB')
    after=hero.crop((350,630,890,1050)).convert('RGB')
    w,h=956,1000
    left=crop_cover(base,(w//2,h),focal=(.37,.48))
    right=crop_cover(after,(w-w//2,h),focal=(.45,.46)).filter(ImageFilter.GaussianBlur(24))
    right=ImageEnhance.Brightness(right).enhance(.55)
    portrait=after.resize((w-w//2-20,round(after.height*(w-w//2-20)/after.width)),Image.Resampling.LANCZOS)
    right.paste(portrait,(10,(h-portrait.height)//2))
    combined=Image.new('RGB',(w,h))
    combined.paste(left,(0,0)); combined.paste(right,(w//2,0))
    combined=ImageEnhance.Contrast(combined).enhance(1.05)
    mask=Image.new('L',(w,h)); md=ImageDraw.Draw(mask)
    md.rounded_rectangle((0,0,w-1,h-1),radius=34,fill=255)
    canvas.paste(combined,(PHOTO[0],PHOTO[1]),mask)
    d=ImageDraw.Draw(canvas)
    mid=PHOTO[0]+w//2
    d.line((mid,PHOTO[1]+18,mid,PHOTO[3]-18),fill='#FFFFFF',width=7)
    d.text((mid+55,PHOTO[1]+750),'ひとつずつ進める',font=font(34),fill='#FFFFFF')
    for x,label,color in ((PHOTO[0]+23,before_label,'#273D48'),(mid+22,after_label,accent)):
        bb=d.textbbox((0,0),label,font=font(35))
        rw=bb[2]+48
        d.rounded_rectangle((x,PHOTO[1]+32,x+rw,PHOTO[1]+100),radius=20,fill=color)
        d.text((x+24,PHOTO[1]+42),label,font=font(35),fill='#FFFFFF' if color!='#40DDCB' else '#062D32')
    d.rounded_rectangle((PHOTO[0]+18,PHOTO[3]-72,PHOTO[0]+300,PHOTO[3]-16),radius=14,fill='#09232B')
    d.text((PHOTO[0]+32,PHOTO[3]-63),'※ イメージ表現',font=font(26),fill='#DAE9E8')
    return canvas

def prepare(root,hero_source,genre='ai_work'):
    root=Path(root);src=root/'source';src.mkdir(parents=True,exist_ok=True)
    first=Image.open(src/'scene_01.png'); second=Image.open(src/'scene_02.png')
    hero=Image.open(hero_source)
    assert hero.width>=900 and hero.height>=1500, 'Independent generated hero source too small'
    slide=draw_hook(first,hero,second,genre)
    slide.save(src/'scene_01_cycle835.png',optimize=True)
    provenance={
      'cycle':835,'change':'Independent full-resolution AI-generated hero used in opening scene; conceptual before/after split',
      'previous':834,'source_original_px':list(hero.size),
      'new_independent_generated_source_count':1,'new_independent_high_res_photos_all_eight':False,
      'new_photo_crop_px':[540,420],'earlier_collage_crop_px':[240,405],
      'scenes_2_to_8':'reused cycle833 scene images','rights':'synthetic AI image; review pending',
      'publication_approved':False,
      'source_sha256':hashlib.sha256(Path(hero_source).read_bytes()).hexdigest()}
    (src/'asset_provenance835.json').write_text(json.dumps(provenance,ensure_ascii=False,indent=2))
    return slide

def render(root):
    root=Path(root);src=root/'source';out=root/'output';out.mkdir(exist_ok=True)
    inputs=[];filters=[]
    for i,n in enumerate(FRAMES):
        path=src/('scene_01_cycle835.png' if i==0 else f'scene_{i+1:02d}.png')
        inputs+=['-i',str(path)]
        x=f'(iw-iw/zoom)*on/{n}' if i%2==0 else f'(iw-iw/zoom)*(1-on/{n})'
        filters.append(f"[{i}:v]zoompan=z='min(1.0+on*0.00015,1.016)':x='{x}':y='(ih-ih/zoom)/2':d={n}:s=1080x1920:fps=30,setsar=1,format=yuv420p[v{i}]")
    filters.append(''.join(f'[v{i}]' for i in range(8))+'concat=n=8:v=1:a=0[vcat]')
    ass=src/'captions832.ass'
    filters.append(f'[vcat]ass={ass}:fontsdir=/usr/share/fonts/opentype/noto[vout]')
    target=out/'cycle835_INDEPENDENT_HERO_SPLIT_JAPANESE_HUMAN_REVIEW.mp4'
    cmd=['ffmpeg','-hide_banner','-loglevel','error','-y','-filter_complex_threads','2',
         *inputs,'-i',str(src/'voice_mastered828.m4a'),'-filter_complex',';'.join(filters),
         '-map','[vout]','-map','8:a:0','-c:v','libx264','-preset','veryfast','-crf','20',
         '-pix_fmt','yuv420p','-r','30','-c:a','aac','-b:a','160k','-ar','48000','-af','apad',
         '-t',str(sum(FRAMES)/30),'-movflags','+faststart',str(target)]
    subprocess.run(cmd,check=True,timeout=240)
    return target

if __name__=='__main__':
    import argparse
    p=argparse.ArgumentParser();p.add_argument('--root',required=True)
    p.add_argument('--hero',required=True);p.add_argument('--genre',default='ai_work')
    a=p.parse_args();prepare(a.root,a.hero,a.genre);print(render(a.root))
