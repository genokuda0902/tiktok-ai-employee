"""Original editorial three-stage visual system. All elements are drawn locally."""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import argparse, json, math
ROOT=Path(__file__).resolve().parents[1]
W,H=1080,1920
FONT='/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc'
REG='/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc'
WHITE=(247,250,255); MUTED=(166,193,208); DARK=(5,19,32)

def font(n,bold=True):return ImageFont.truetype(FONT if bold else REG,n)
def txt(d,xy,s,n,c=WHITE,bold=True,anchor=None):d.text(xy,s,font=font(n,bold),fill=c,anchor=anchor)
def rr(d,box,r,fill,outline=None,w=1):d.rounded_rectangle(box,radius=r,fill=fill,outline=outline,width=w)
def color(s):return tuple(bytes.fromhex(s.lstrip('#')))
def mix(a,b,t):return tuple(round(a[i]*(1-t)+b[i]*t) for i in range(3))
def background():
    im=Image.new('RGB',(W,H));d=ImageDraw.Draw(im)
    for y in range(H):d.line((0,y,W,y),fill=mix((2,11,24),(9,31,48),y/H))
    for x in range(64,1050,78):d.line((x,215,x,1570),fill=(15,41,56))
    for y in range(228,1560,78):d.line((50,y,1030,y),fill=(15,41,56))
    return im

def get_genres():return json.loads((ROOT/'config/genres.json').read_text(encoding='utf8'))['genres']
def create(stage=1,genre='雑学・科学',title='「2＋3」はどうなる？',steps=None):
    """Render three distinct 1080x1920 PNG states; pass genre-specific content explicitly."""
    if stage not in (1,2,3):raise ValueError('stage must be 1, 2, or 3')
    styles={g['name']:g for g in get_genres()}
    if genre not in styles:raise ValueError('Unknown genre')
    if steps is None:steps=[('入力','2 ＋ 3','数字を受け取る'),('処理','CPU','足し算をする'),('出力','5','答えを表示')]
    if len(steps)!=3:raise ValueError('Exactly three steps required')
    accent=color(styles[genre]['accent']);im=background();d=ImageDraw.Draw(im)
    rr(d,(55,61,402,137),18,(6,57,69),accent,3);txt(d,(81,76),'15秒でわかる',42)
    txt(d,(1010,92),'06 / 08',29,MUTED,False,'ra')
    rr(d,(55,169,1025,182),7,(28,62,75));rr(d,(55,169,760,182),7,accent)
    txt(d,(57,242),'入力 → 処理 → 出力',64)
    txt(d,(60,342),title,40,MUTED,False)
    rr(d,(54,454,1024,1259),38,(3,27,42),(59,121,135),4)
    # Larger vertically stacked modules preserve legibility on a phone.
    for i,(label,value,desc) in enumerate(steps):
        y=489+i*250;active=(stage==i+1)
        if active:
            halo=Image.new('RGBA',(W,H),(0,0,0,0));hd=ImageDraw.Draw(halo)
            hd.rounded_rectangle((73,y-5,1004,y+224),radius=32,fill=(*accent,55))
            halo=halo.filter(ImageFilter.GaussianBlur(18));im=Image.alpha_composite(im.convert('RGBA'),halo).convert('RGB');d=ImageDraw.Draw(im)
        rr(d,(80,y,997,y+216),29,(10,59,69) if active else (6,35,49),accent if active else (42,89,105),5 if active else 2)
        rr(d,(101,y+31,207,y+116),20,accent if active else (24,64,78))
        txt(d,(154,y+72),f'{i+1:02d}',44,DARK if active else MUTED,True,'mm')
        txt(d,(245,y+25),label,33,accent if active else MUTED)
        value_size=102 if i==2 else 78
        txt(d,(247,y+83),value,value_size,WHITE if active else (186,204,216))
        txt(d,(835,y+116),desc,26,accent if active else MUTED,False,'mm')
        if i<2:
            # The connector is a subtle editorial cue, not a busy animation.
            d.polygon([(529,y+223),(550,y+239),(571,y+223)],fill=accent if active else (55,107,116))
    rr(d,(55,1323,1019,1540),28,(4,23,42),(108,180,246),4)
    rr(d,(71,1340,1001,1524),21,(7,39,61))
    rr(d,(91,1355,296,1405),12,(57,108,140));txt(d,(108,1366),'VOICE / JP',27)
    txt(d,(949,1371),'11 / 16' if stage<=2 else '12 / 16',25,(145,197,234),False,'ra')
    txt(d,(534,1439),'入力、処理、' if stage<=2 else '出力。',64,WHITE,True,'mm')
    rr(d,(94,1504,968,1517),7,(24,86,107));rr(d,(94,1504,460 if stage==1 else 695 if stage==2 else 962,1517),7,(111,199,255))
    txt(d,(70,1631),'INPUT  →  PROCESS  →  OUTPUT',30,accent)
    txt(d,(70,1693),'数字を受け取り、計算して、答えを表示。',31,MUTED,False)
    # Leave bottom 200px visually quiet for TikTok overlay UI.
    return im

def main():
    p=argparse.ArgumentParser();p.add_argument('--genre',default='雑学・科学');p.add_argument('--output-dir',default=str(ROOT/'assets'))
    a=p.parse_args();out=Path(a.output_dir);out.mkdir(parents=True,exist_ok=True)
    for i in (1,2,3):
        path=out/f'scene06_{i}.png';create(i,a.genre).save(path,optimize=True);print(path)
if __name__=='__main__':main()
