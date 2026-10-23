"""cycle799: original 14.0–17.2s dual-verification scene, review-only.
Reimplementation, not recovered v33 code. No user media or private assets.
"""
import argparse,json,subprocess
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
W,H,FPS,FRAMES=1080,1920,30,96
START_FRAME,END_FRAME=420,516
FONT='/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc'
BOLD='/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc'

def validate(c):
    if c.get('mode')!='review_only':raise ValueError('review only')
    if any(c.get(k) is not False for k in ('rights_reviewed','employee_approved','publication_approved')):raise ValueError('approval must fail closed')
    if len(set(c.get('genres',[])))!=10:raise ValueError('ten genres required')
    vals=c.get('values',[])
    if len(vals)!=4 or any(type(v) is not int or v<0 for v in vals):raise ValueError('four nonnegative integers')
    if sum(vals)!=c.get('total'):raise ValueError('inconsistent total')
    if c.get('formula')!='=SUM(B2:B5)':raise ValueError('invalid formula')
    if not c.get('title') or not c.get('disclaimer'):raise ValueError('disclosure/title missing')
    return True

def f(size,bold=False):return ImageFont.truetype(BOLD if bold else FONT,size)
def label(d,xy,s,size=36,color='#f1fbff',bold=False,anchor=None):d.text(xy,s,font=f(size,bold),fill=color,anchor=anchor)
def box(d,rect,fill,outline=None,radius=24,width=2):d.rounded_rectangle(rect,radius=radius,fill=fill,outline=outline,width=width)
def ease(t):
    t=max(0,min(1,t));return t*t*(3-2*t)
def safe_boxes():
    return {'headline':(80,246,1000,398),'manual':(80,442,1000,850),'sheet':(80,907,1000,1317),'result':(80,1373,1000,1557),'disclaimer':(80,1595,1000,1658)}
def background():
    import numpy as np
    yy=np.arange(H,dtype=np.float32)[:,None]
    xx=np.arange(W,dtype=np.float32)[None,:]
    light=np.exp(-((xx-860)**2/(570**2)+(yy-610)**2/(1000**2)))*0.8
    arr=np.empty((H,W,3),dtype=np.uint8)
    arr[:,:,0]=(7+9*light+2*yy/H).astype('uint8')
    arr[:,:,1]=(18+25*light+4*yy/H).astype('uint8')
    arr[:,:,2]=(33+31*light+7*yy/H).astype('uint8')
    return Image.fromarray(arr,'RGB')
def make_frame(i,c,bg=None):
    validate(c)
    if not 0<=i<FRAMES:raise ValueError('frame out of bounds')
    im=(bg if bg is not None else background()).copy();d=ImageDraw.Draw(im)
    teal='#36dfca';white='#f5fbff';muted='#9fb9c9'
    for y in range(250,1640,92):d.line((80,y,1000,y),fill='#18334a',width=1)
    stage1=ease((i-6)/22);stage2=ease((i-35)/24);stage3=ease((i-68)/18)
    box(d,(80,145,418,208),'#123c4a','#27978f',20)
    label(d,(101,155),'AI時短ラボ / DEMO',27,teal,True)
    label(d,(80,252),c['title'],49,white,True)
    label(d,(82,342),'同じ数値を、2つの方法で確認',31,muted)
    box(d,(80,442,1000,850),'#122d42','#35647a',34,3)
    box(d,(104,462,355,529),'#304b62',radius=19)
    label(d,(128,472),'01  手計算',35,white,True)
    label(d,(125,553),'12万 + 15万 + 20万 + 18万',39,white,True)
    d.line((125,643,949,643),fill='#32556b',width=3)
    label(d,(126,677),'合計',34,muted)
    label(d,(948,667),'650,000 円' if stage1>.9 else '計算中…',62,teal if stage1>.9 else muted,True,'ra')
    d.rounded_rectangle((126,779,126+int(819*stage1),792),radius=6,fill=teal)
    box(d,(80,907,1000,1317),'#f2f9fc','#37b7ab',34,3)
    box(d,(104,927,463,996),'#176f66',radius=19)
    label(d,(126,937),'02  表計算の式',34,white,True)
    box(d,(125,1026,955,1115),'#dcebf1',radius=13)
    label(d,(151,1035),c['formula'],48,'#153f54',True)
    label(d,(126,1164),'計算結果',35,'#34546b')
    label(d,(948,1154),'650,000 円' if stage2>.9 else '処理中…',59,'#087e6b' if stage2>.9 else '#8aa5b5',True,'ra')
    d.rounded_rectangle((126,1272,126+int(819*stage2),1285),radius=6,fill='#0ea48e')
    box(d,(80,1373,1000,1557),'#123b46','#32bcb1',30,3)
    if stage3>.05:
        box(d,(111,1406,969,1517),'#175a59',radius=22)
        label(d,(540,1416),'✓  一致  650,000 円',57,white,True,'ma')
    else:label(d,(540,1418),'2つの計算結果を照合',42,muted,True,'ma')
    label(d,(80,1603),c['disclaimer'],26,muted)
    return im
def render_segment(c,out):
    validate(c);out=Path(out);out.parent.mkdir(parents=True,exist_ok=True)
    bg=background()
    cmd=['ffmpeg','-hide_banner','-loglevel','error','-y','-f','rawvideo','-pix_fmt','rgb24','-s',f'{W}x{H}','-r',str(FPS),'-i','-','-c:v','libx264','-preset','ultrafast','-crf','21','-pix_fmt','yuv420p','-movflags','+faststart',str(out)]
    p=subprocess.Popen(cmd,stdin=subprocess.PIPE,stderr=subprocess.PIPE)
    try:
        for i in range(FRAMES):p.stdin.write(make_frame(i,c,bg).tobytes())
        p.stdin.close();err=p.stderr.read().decode(errors='replace');rc=p.wait()
        if rc:raise RuntimeError('ffmpeg: '+err[-1200:])
    finally:
        if p.poll() is None:p.kill()
    return out
def splice(src,seg,out):
    graph=(f'[0:v]trim=start_frame=0:end_frame={START_FRAME},setpts=PTS-STARTPTS[v0];'
           '[1:v]setpts=PTS-STARTPTS[v1];'
           f'[0:v]trim=start_frame={END_FRAME}:end_frame=714,setpts=PTS-STARTPTS[v2];'
           '[v0][v1][v2]concat=n=3:v=1:a=0[v];[v]fps=30,setpts=N/(30*TB)[vout]')
    subprocess.run(['ffmpeg','-hide_banner','-loglevel','error','-y','-i',str(src),'-i',str(seg),'-filter_complex',graph,'-map','[vout]','-map','0:a:0','-c:v','libx264','-preset','veryfast','-crf','20','-pix_fmt','yuv420p','-c:a','copy','-movflags','+faststart',str(out)],check=True)
def main():
    p=argparse.ArgumentParser();p.add_argument('--config',required=True);p.add_argument('--segment',required=True);p.add_argument('--source');p.add_argument('--output');a=p.parse_args()
    c=json.loads(Path(a.config).read_text(encoding='utf-8'))
    render_segment(c,a.segment)
    if a.source:
        if not a.output:p.error('--output required with --source')
        splice(a.source,a.segment,a.output)
if __name__=='__main__':main()
