"""cycle940: three-beat legible finished-example preview; private review only.

Synthetic illustration, not a ChatGPT/Excel screen recording. Never uploads or posts.
"""
from __future__ import annotations
import argparse, hashlib, json, subprocess
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageFilter

WIDTH, HEIGHT, FPS, FRAMES = 1080, 1920, 30, 691
START, COUNT, SAFE_Y = 174, 87, 1445
POLICY = 'HUMAN_REVIEW / PUBLICATION_NOT_APPROVED'
BOLD = '/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc'
REGULAR = '/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc'
GENRES = {
    'ai_work': ('月次レポート', '営業A', '営業B'),
    'business': ('週次レポート', '作業A', '作業B'),
    'finance': ('家計メモ', '収入', '支出'),
    'education': ('学習メモ', '単元A', '単元B'),
    'health': ('生活記録', '項目A', '項目B'),
    'beauty': ('予約表', '予約A', '予約B'),
    'food': ('発注表', '商品A', '商品B'),
    'travel': ('旅程表', '予定A', '予定B'),
    'lifestyle': ('家事表', '家事A', '家事B'),
    'technology': ('作業ログ', '工程A', '工程B'),
}

def sha256(path):
    h=hashlib.sha256()
    with open(path,'rb') as f:
        for chunk in iter(lambda:f.read(1<<20),b''): h.update(chunk)
    return h.hexdigest()

def guard(genre, expected_sha):
    if genre not in GENRES or len(GENRES)!=10: raise ValueError('unsupported genre')
    if not isinstance(expected_sha,str) or len(expected_sha)!=64 or any(c not in '0123456789abcdef' for c in expected_sha):
        raise ValueError('pinned full lowercase SHA256 required')
    if not (SAFE_Y<=1450 and START==174 and COUNT==87 and POLICY.endswith('PUBLICATION_NOT_APPROVED')):
        raise RuntimeError('safe-area or approval guard failed')
    if not (Path(BOLD).exists() and Path(REGULAR).exists()): raise FileNotFoundError('Noto CJK fonts missing')

def stage(i):
    if not 0<=i<COUNT: raise ValueError('frame outside scene03')
    return i//29

def f(size,bold=False):return ImageFont.truetype(BOLD if bold else REGULAR,size)

def make_frame(i,genre='ai_work'):
    if genre not in GENRES:raise ValueError('unsupported genre')
    p=stage(i)
    title,c1,c2=GENRES[genre]
    im=Image.new('RGB',(WIDTH,SAFE_Y),(6,21,38));d=ImageDraw.Draw(im)
    for y in range(SAFE_Y):
        d.line((0,y,WIDTH,y),fill=(6+int(y/SAFE_Y*7),21+int(y/SAFE_Y*17),38+int(y/SAFE_Y*19)))
    # Cinematic soft light bloom; native-resolution UI and text are drawn afterward.
    glow=Image.new('RGBA',(WIDTH,SAFE_Y),(0,0,0,0));g=ImageDraw.Draw(glow)
    g.ellipse((-270,-400,720,500),fill=(25,171,188,110))
    g.ellipse((660,580,1420,1400),fill=(33,108,177,85))
    im=Image.alpha_composite(im.convert('RGBA'),glow.filter(ImageFilter.GaussianBlur(125))).convert('RGB')
    d=ImageDraw.Draw(im)
    d.rounded_rectangle((45,55,1035,148),radius=23,fill='#123A52',outline='#4DADB7',width=2)
    d.text((75,73),'AI WORK / 03   •   完成形の見本',font=f(41,True),fill='#F3FFFF')
    d.text((61,187),'最初に「完成形」を決める',font=f(58,True),fill='#FFFFFF')
    d.text((62,272),'架空の出力見本・実際のアプリ画面ではありません',font=f(29),fill='#B5D4DE')
    # Large paper with clear, staged focus instead of tiny unreadable report.
    d.rounded_rectangle((58,358,1022,1160),radius=37,fill='#D4E5E9')
    d.rounded_rectangle((75,337,1005,1135),radius=31,fill='#F7FAFB',outline='#8DD3D8',width=4)
    d.rounded_rectangle((110,375,968,476),radius=22,fill='#0E425A')
    d.text((147,394),title,font=f(51,True),fill='#FFFFFF')
    d.text((795,407),'見本 / DEMO',font=f(26,True),fill='#89E8E3')
    headers=['期間',c1,c2,'確認']
    xs=[135,356,578,802]
    d.rounded_rectangle((109,520,968,601),radius=14,fill='#D5E9EC')
    for x,t in zip(xs,headers):d.text((x,534),t,font=f(35,True),fill='#163B50')
    for row,(period,v1,v2,check) in enumerate([('4月','12','8','未確認'),('5月','16','9','未確認'),('6月','18','12','確認待ち')]):
        y=632+row*124
        d.rounded_rectangle((110,y,968,y+104),radius=14,fill='#E9F3F5' if row%2==0 else '#FFFFFF')
        for x,t in zip(xs,[period,v1,v2,check]):d.text((x,y+22),t,font=f(36,True if row==2 else False),fill='#18394B')
    # Phase 0: preview, phase 1: required columns, phase 2: human verification.
    if p==0:
        box=(108,369,970,483);headline='① 完成形を見せる';detail='どんな表にしたいか、先に決める'
    elif p==1:
        box=(107,515,969,602);headline='② 必要な項目を示す';detail='期間・数字・確認欄を指定する'
    else:
        box=(768,873,970,1100);headline='③ 人が確認する';detail='出力結果を元データと照合する'
    # Gentle animated highlight; no glyph movement or blur.
    pulse=4+int(3*abs((i%29)-14)/14)
    d.rounded_rectangle(box,radius=19,outline='#16C3B9',width=pulse)
    d.rounded_rectangle((75,1190,1005,1365),radius=24,fill='#0F5162',outline='#5CE0D4',width=3)
    d.text((111,1214),headline,font=f(51,True),fill='#FFFFFF')
    d.text((111,1290),detail,font=f(34),fill='#C8F6F0')
    for j in range(3):
        d.rounded_rectangle((383+j*109,1403,468+j*109,1418),radius=7,fill='#6CE6D6' if j==p else '#355C6D')
    # Top only; inherited Japanese burned-in subtitles below SAFE_Y remain untouched.
    return im

def run(source,output,tmp,genre,expected_sha):
    guard(genre,expected_sha)
    source=Path(source);output=Path(output);tmp=Path(tmp)
    if not source.is_file():raise FileNotFoundError(source)
    if source.resolve()==output.resolve():raise ValueError('source overwrite forbidden')
    if sha256(source)!=expected_sha:raise RuntimeError('FAIL_CLOSED_SOURCE_SHA_MISMATCH')
    tmp.mkdir(parents=True,exist_ok=True);output.parent.mkdir(parents=True,exist_ok=True)
    overlay=tmp/'overlays';overlay.mkdir(exist_ok=True)
    for i in range(COUNT):make_frame(i,genre).save(overlay/f'{i:03d}.png',compress_level=1)
    graph=f"[1:v]setpts=PTS+{START}/{FPS}/TB[ov];[0:v][ov]overlay=0:0:eof_action=pass:enable='between(n,{START},{START+COUNT-1})'[v]"
    cmd=['ffmpeg','-hide_banner','-loglevel','error','-y','-i',str(source),'-framerate',str(FPS),'-start_number','0','-i',str(overlay/'%03d.png'),'-filter_complex',graph,'-map','[v]','-map','0:a:0','-c:v','libx264','-preset','veryfast','-crf','21','-pix_fmt','yuv420p','-r',str(FPS),'-frames:v',str(FRAMES),'-c:a','copy','-movflags','+faststart',str(output)]
    proc=subprocess.run(cmd,capture_output=True,text=True)
    (tmp/'ffmpeg_encode.log').write_text(proc.stderr,encoding='utf-8')
    if proc.returncode:raise RuntimeError('ffmpeg encode failed: '+proc.stderr[-1000:])
    result={'policy':POLICY,'source_sha256':expected_sha,'output_sha256':sha256(output),'edited_frames':[START,START+COUNT-1],'genre':genre,'genre_profiles':len(GENRES),'synthetic_illustration':True,'independent_japanese_asr':'NOT_VERIFIED','publication_allowed':False}
    (tmp/'render_result.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
    return result

if __name__=='__main__':
    ap=argparse.ArgumentParser()
    for name in ('source','output','tmp','expected-source-sha'):ap.add_argument('--'+name,required=True)
    ap.add_argument('--genre',choices=GENRES,default='ai_work')
    a=ap.parse_args()
    print(json.dumps(run(a.source,a.output,a.tmp,a.genre,a.expected_source_sha),ensure_ascii=False))
