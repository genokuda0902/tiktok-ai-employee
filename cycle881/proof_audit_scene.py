"""cycle881 review-only synthetic data proof. Original v33 code is NOT recovered."""
from __future__ import annotations
from dataclasses import dataclass, replace
from functools import lru_cache
from pathlib import Path
import argparse, hashlib, json, subprocess, tempfile

FPS=30
W,H=1080,1920
TOP_HEIGHT=1450
START,END,TOTAL=336,422,691
CAPTION_SAFE_Y=1450
GENRES=('ai_work','money','career','learning','health_general','travel',
        'food','beauty_general','home','technology')
POLICY={'review_only':True,'publication_approved':False,'external_upload':False,
        'automatic_posting':False,'source_rights_reviewed':False}

@dataclass(frozen=True)
class Proof:
    genre:str
    title:str
    source_name:str
    columns:tuple[str,str]
    months:tuple[str,str,str]
    data:tuple[tuple[int,int],tuple[int,int],tuple[int,int]]
    expected:tuple[int,int]
    footer:str

DEFAULT=Proof('ai_work','AIの回答を、元データで検算','月別売上（架空データ）',
              ('営業A','営業B'),('4月','5月','6月'),((12,8),(16,9),(18,12)),
              (46,29),'数字は元データと必ず照合')
CAPTIONS=(
 ('AIで仕事を早くするなら、最初の一歩が大事。',.27,2.93),
 ('まず、繰り返している作業を書き出そう。',3.31,5.60),
 ('次に、完成形の見本を用意する。',5.90,8.23),
 ('指示は、目的と条件を具体的に伝える。',8.52,11.10),
 ('最初の出力は、必ず自分で確かめる。',11.41,13.97),
 ('違いがあれば、修正点を一つずつ伝える。',14.28,16.93),
 ('使える指示は、テンプレートに残す。',17.26,19.50),
 ('小さな時短を、毎日の習慣にしよう。',19.86,22.55),
)

def sha256(path):
    h=hashlib.sha256()
    with open(path,'rb') as f:
        for part in iter(lambda:f.read(1024*1024),b''):h.update(part)
    return h.hexdigest()

def validate_proof(p):
    if p.genre not in GENRES:raise ValueError('genre')
    if len(p.columns)!=2 or len(p.months)!=3 or len(p.data)!=3:raise ValueError('shape')
    if any(len(row)!=2 or any(type(x)!=int or x<0 or x>9999 for x in row) for row in p.data):
        raise ValueError('data')
    sums=tuple(sum(row[i] for row in p.data) for i in range(2))
    if sums!=p.expected:raise ValueError('unsupported total')
    for value in (p.title,p.source_name,*p.columns,*p.months,p.footer):
        if not value or len(value)>32 or any(x in value for x in ('@','https://','http://','LINE ID','電話番号')):
            raise ValueError('unsafe copy')
    return sums

def validate_manifest(source,manifest):
    if manifest!={**POLICY,'source_sha256':sha256(source)}:
        raise ValueError('unapproved or mismatched private input')
    return True

def review_caption_alignment(captions,independent_transcript=None,reviewer_approved=False):
    """Independent transcript required; original subtitle script is NOT ASR."""
    if independent_transcript is None or not reviewer_approved:
        return {'semantic_match_verified':False,'status':'HUMAN_REVIEW_REQUIRED'}
    if len(captions)!=len(independent_transcript):
        return {'semantic_match_verified':False,'status':'MISMATCH'}
    for (text,s,e),(spoken,ss,ee) in zip(captions,independent_transcript):
        if text.replace(' ','')!=spoken.replace(' ','') or abs(s-ss)>.30 or abs(e-ee)>.30:
            return {'semantic_match_verified':False,'status':'MISMATCH'}
    return {'semantic_match_verified':True,'status':'TEXT_TIMING_MATCH_HUMAN_REVIEWED',
            'pronunciation_verified':False}

def progress(n):
    if not 0<=n<END-START:raise ValueError('frame')
    return min(2,n//28)

@lru_cache(maxsize=1)
def fonts():
    from PIL import ImageFont
    bold='/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc'
    reg='/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc'
    return {('b',n):ImageFont.truetype(bold,n) for n in (30,34,40,43,51,62)} | {
            ('r',n):ImageFont.truetype(reg,n) for n in (30,32,36)}

def frame_image(n,p=DEFAULT):
    from PIL import Image,ImageDraw,ImageFilter
    validate_proof(p);phase=progress(n)
    im=Image.new('RGB',(W,TOP_HEIGHT),(7,19,35))
    glow=Image.new('RGBA',(W,TOP_HEIGHT),(0,0,0,0));g=ImageDraw.Draw(glow)
    g.ellipse((460,-330,1450,760),fill=(29,119,173,95))
    g.ellipse((-420,550,470,1440),fill=(12,178,162,47))
    im=Image.alpha_composite(im.convert('RGBA'),glow.filter(ImageFilter.GaussianBlur(160))).convert('RGB')
    d=ImageDraw.Draw(im);F=fonts();B=lambda size:F['b',size];R=lambda size:F['r',size]
    d.rounded_rectangle((53,37,443,106),radius=24,fill=(12,63,77),outline=(66,173,190),width=2)
    d.text((77,53),'SOURCE  /  PROOF  05',font=B(30),fill=(225,248,252))
    d.text((884,55),'05 / 08',font=B(30),fill=(113,232,233))
    d.text((61,157),p.title,font=B(51),fill=(249,252,255))
    d.text((65,248),'「AIが言った」だけでは終わらせない',font=R(32),fill=(158,221,231))
    d.rounded_rectangle((54,330,1025,827),radius=26,fill=(10,32,52),outline=(45,114,141),width=3)
    d.rounded_rectangle((75,354,1004,419),radius=15,fill=(13,88,105))
    d.text((100,367),p.source_name,font=B(34),fill=(243,253,255))
    xs=(115,490,776)
    for x,label in zip(xs,('月',*p.columns)):
        d.text((x,451),label,font=B(40),fill=(188,241,248))
    for i,(month,values) in enumerate(zip(p.months,p.data)):
        y=524+i*89;active=phase==0 and (n//9)%3==i
        d.rounded_rectangle((86,y-8,995,y+75),radius=12,
          fill=(24,91,105) if active else (20,50,68),
          outline=(83,205,204) if active else (29,69,90),width=2)
        for x,value in zip(xs,(month,*values)):
            d.text((x,y+3),str(value),font=B(43),
                   fill=(255,252,228) if active else (244,253,255))
    d.rounded_rectangle((55,863,1025,1220),radius=27,fill=(8,28,48),outline=(37,113,136),width=3)
    if phase==0:
        d.text((94,899),'01  元データを読む',font=B(43),fill=(104,237,223))
        d.text((99,984),'4月・5月・6月の3行を確認',font=B(40),fill=(249,253,255))
        d.text((99,1064),'架空データ ／ 実サービス操作ではありません',font=R(30),fill=(175,213,222))
    elif phase==1:
        d.text((94,899),'02  AIの集計結果',font=B(43),fill=(104,237,223))
        d.text((99,978),f'{p.columns[0]}  {p.expected[0]}',font=B(62),fill=(248,250,255))
        d.text((588,978),f'{p.columns[1]}  {p.expected[1]}',font=B(62),fill=(248,250,255))
        d.text((99,1087),'この数値は、まだ確認中',font=R(36),fill=(255,195,122))
    else:
        d.text((94,899),'03  元データから検算',font=B(43),fill=(104,237,223))
        for i in range(2):
            eq='+'.join(str(row[i]) for row in p.data)+f' = {p.expected[i]}'
            d.text((99,971+i*91),f'{p.columns[i]}  {eq}',font=B(43),fill=(244,253,255))
        d.rounded_rectangle((814,888,989,950),radius=15,fill=(18,135,116))
        d.text((844,900),'一致',font=B(34),fill=(249,255,255))
    d.text((69,1353),p.footer,font=B(34),fill=(199,239,244))
    return im

def render(source,output,manifest,p=DEFAULT,ffmpeg='ffmpeg'):
    source=Path(source);output=Path(output)
    if not source.is_file() or output.exists():raise ValueError('source missing or output exists')
    validate_manifest(source,manifest);validate_proof(p)
    with tempfile.TemporaryDirectory(prefix='cycle881_') as td:
        folder=Path(td)
        for n in range(END-START):
            frame_image(n,p).save(folder/f'proof_{n:04d}.png',compress_level=2)
        cmd=[ffmpeg,'-hide_banner','-loglevel','error','-nostdin','-y',
          '-i',str(source),'-itsoffset',str(START/FPS),'-framerate',str(FPS),
          '-i',str(folder/'proof_%04d.png'),
          '-filter_complex','[0:v][1:v]overlay=x=0:y=0:shortest=0:eof_action=pass:format=auto[v]',
          '-map','[v]','-map','0:a:0','-c:v','libx264','-preset','veryfast',
          '-crf','19','-pix_fmt','yuv420p','-r',str(FPS),'-frames:v',str(TOTAL),
          '-c:a','copy','-movflags','+faststart',str(output)]
        subprocess.run(cmd,check=True,timeout=300)
    return {'source_sha256':sha256(source),'output_sha256':sha256(output),
            'scene_start':START,'scene_end_exclusive':END,'caption_safe_y':CAPTION_SAFE_Y,
            'genre':p.genre,'caption_review':review_caption_alignment(CAPTIONS),
            'source_rights_verified':False,'policy':POLICY}

if __name__=='__main__':
    parser=argparse.ArgumentParser()
    for name in ('source','output','manifest','report'):parser.add_argument('--'+name,required=True)
    a=parser.parse_args();manifest=json.loads(Path(a.manifest).read_text(encoding='utf-8'))
    result=render(a.source,a.output,manifest)
    Path(a.report).write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
    print(json.dumps(result,ensure_ascii=False))
