"""Cycle589: original, synthetic spreadsheet evidence insert. Review only."""
from dataclasses import dataclass
from pathlib import Path
import argparse, subprocess
from PIL import Image, ImageDraw, ImageFont
W,H,FPS,SECONDS=1080,1920,30,3
GENRES={'AI・仕事効率化':'#29d6c5','美容・身だしなみ':'#f6a8d2','恋愛・心理':'#f6aa9b','お金・節約':'#f0d57a','営業・ビジネス':'#53bff0','転職・キャリア':'#bca5f8','健康・生活改善':'#82dca5','雑学・科学':'#68dce4','旅行・グルメ':'#f2c18a','商品比較・暮らし':'#a5c9ff'}
FONT='/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc'
@dataclass(frozen=True)
class Proof:
    genre:str='AI・仕事効率化'
    values:tuple[int,...]=(120,150,200,250)
    months:tuple[str,...]=('1月','2月','3月','4月')
    claimed_total:int=720
    subtitle:str='B2:B5を選択 → 合計を検算'
def validate(p):
    if p.genre not in GENRES:raise ValueError('unknown genre')
    if not 1<=len(p.values)<=6 or len(p.values)!=len(p.months):raise ValueError('invalid rows')
    if any(type(v)!=int or v<0 for v in p.values):raise ValueError('invalid values')
    if sum(p.values)!=p.claimed_total:raise ValueError('incorrect total')
    if len(p.subtitle)>28:raise ValueError('caption too long')
    return True
def render_frame(frame,p=Proof()):
    validate(p)
    if not 0<=frame<FPS*SECONDS:raise ValueError('bad frame')
    t=frame/FPS; a=tuple(bytes.fromhex(GENRES[p.genre][1:]))
    im=Image.new('RGB',(W,H),(9,21,37));d=ImageDraw.Draw(im)
    def tx(x,y,s,size=32,c=(238,247,250)):
        d.text((x,y),s,font=ImageFont.truetype(FONT,size),fill=c)
    def card(box,fill,outline=None,r=18):
        d.rounded_rectangle(box,radius=r,fill=fill,outline=outline,width=3)
    card((62,80,1018,154),(20,56,71),(44,101,117))
    tx(92,94,'STEP 03 / SPREADSHEET PROOF',29,(169,217,229))
    tx(70,202,'実際の表に近い画面で',53)
    tx(70,280,'合計を検算する',67,a)
    tx(75,380,'架空データによる操作再現',29,(172,193,202))
    # Synthetic spreadsheet, not a captured commercial UI.
    card((60,470,1020,1310),(245,249,250),(106,153,162))
    d.rectangle((61,472,1019,540),fill=(39,55,66))
    tx(225,486,'月次売上 / SAMPLE DATA',30)
    for i,c in enumerate(((246,103,103),(245,203,92),(100,204,149))):
        d.ellipse((92+i*33,498,107+i*33,513),fill=c)
    d.rectangle((61,540,1019,612),fill=(226,236,238))
    tx(89,551,'ファイル  編集  表示  挿入  データ',26,(65,82,93))
    d.rectangle((61,612,1019,681),fill=(248,250,251))
    tx(91,625,'B2:B5',29,(30,62,74))
    tx(267,625,'fx',29,(27,132,142))
    formula='=SUM(B2:B5)'
    if t<1:formula=''
    elif t<2:formula=formula[:int((t-1)*len(formula))]
    tx(338,625,formula,29,(25,52,62))
    x0,y0=109,683; cw=[68,200,220,220,220]; xs=[x0]
    for width in cw:xs.append(xs[-1]+width)
    for r in range(9):
        y=y0+r*72
        if r==0:d.rectangle((61,y,1019,y+72),fill=(226,237,240))
        d.line((61,y,1019,y),fill=(184,207,213),width=2)
    for x in xs:d.line((x,y0,x,y0+576),fill=(184,207,213),width=2)
    for i,c in enumerate('ABCD'):tx(xs[i+1]+34,y0+14,c,28,(61,85,96))
    for r in range(1,8):tx(79,y0+r*72+16,str(r),25,(79,100,109))
    tx(xs[1]+22,y0+87,'月',28,(38,63,71))
    tx(xs[2]+22,y0+87,'売上',28,(38,63,71))
    for i,(month,value) in enumerate(zip(p.months,p.values)):
        yy=y0+(i+2)*72+13
        tx(xs[1]+23,yy,month,30,(35,62,73))
        tx(xs[2]+29,yy,str(value),31,(35,62,73))
    total_y=y0+(len(p.values)+2)*72
    tx(xs[1]+23,total_y+13,'合計',30,(35,62,73))
    if t>=2:
        d.rectangle((xs[2]+2,total_y+2,xs[3]-2,total_y+69),fill=(204,243,233))
        tx(xs[2]+29,total_y+12,str(p.claimed_total),33,(18,115,98))
    n=min(len(p.values),max(0,int((t-.12)/.18)+1)) if t<1 else len(p.values)
    if n:d.rectangle((xs[2]+2,y0+146,xs[3]-2,y0+(n+2)*72-2),outline=a,width=6)
    tx(75,1397,'CHECK / 数値の根拠',30,(167,193,202))
    card((70,1472,1010,1696),(16,46,61),a)
    if t<1:label,detail='範囲を選択中','B2:B5'
    elif t<2:label,detail='関数を入力','=SUM(B2:B5)'
    else:label,detail='検算した合計',str(p.claimed_total)
    tx(107,1502,label,45)
    tx(107,1585,detail,70 if t>=2 else 46,a)
    card((70,1740,1010,1842),(14,34,47))
    tx(125,1760,p.subtitle,39)
    tx(80,1870,'DEMO / 架空データ / REVIEW ONLY',23,(128,159,170))
    return im
def render_insert(out,p=Proof()):
    validate(p);out=Path(out);out.parent.mkdir(parents=True,exist_ok=True)
    cmd=['ffmpeg','-v','error','-y','-f','rawvideo','-pixel_format','rgb24','-video_size',f'{W}x{H}','-framerate',str(FPS),'-i','-','-c:v','libx264','-preset','ultrafast','-crf','17','-pix_fmt','yuv420p',str(out)]
    proc=subprocess.Popen(cmd,stdin=subprocess.PIPE)
    for i in range(FPS*SECONDS):proc.stdin.write(render_frame(i,p).tobytes())
    proc.stdin.close()
    if proc.wait():raise RuntimeError('insert encode failed')
    return out
def compose(baseline,insert,out):
    baseline,insert,out=map(Path,(baseline,insert,out))
    if not baseline.exists():raise FileNotFoundError(baseline)
    graph='[1:v]setpts=PTS-STARTPTS+9/TB[i];[0:v][i]overlay=eof_action=pass:shortest=0[v]'
    cmd=['ffmpeg','-v','error','-y','-i',str(baseline),'-i',str(insert),'-filter_complex',graph,'-map','[v]','-map','0:a:0','-c:v','libx264','-preset','ultrafast','-crf','19','-pix_fmt','yuv420p','-r','30','-frames:v','600','-c:a','copy','-movflags','+faststart',str(out)]
    subprocess.run(cmd,check=True);return out
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--baseline',type=Path);p.add_argument('--out',type=Path,default=Path('cycle589_REVIEW_ONLY.mp4'));p.add_argument('--insert',type=Path,default=Path('cycle589_insert.mp4'))
    a=p.parse_args();render_insert(a.insert)
    if a.baseline:compose(a.baseline,a.insert,a.out)
