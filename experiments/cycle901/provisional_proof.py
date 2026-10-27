"""Cycle901 provisional evidence; private, review-only video.
Core policy is stdlib-only. Pillow+ffmpeg needed for local rendering.
"""
from pathlib import Path
import argparse,subprocess,json
GENRES=('ai_work','business','education','science','history','finance','cooking','wellness','travel','storytelling')
STATUS={'provisional':'検証前の仮集計','verified':'元データ照合済み','rejected':'数値の再確認が必要'}
POLICY='HUMAN_REVIEW / PUBLICATION_NOT_APPROVED'
X,Y,W,H=30,130,900,510
START,END=5.667,8.367
def sum_evidence(rows):
    if not rows or len(rows)>12 or any(type(a) is not int or type(b) is not int or a<0 or b<0 for a,b in rows):
        raise ValueError('nonnegative integer evidence required')
    return sum(a for a,_ in rows),sum(b for _,b in rows)
def validate_proof(*,genre,state,displayed,source=None,approved=False,contains_private_data=False):
    if genre not in GENRES or state not in STATUS:raise ValueError('unsupported genre or state')
    if approved or contains_private_data:raise ValueError('private material/release forbidden')
    if len(displayed)!=2 or any(type(v) is not int or v<0 for v in displayed):raise ValueError('invalid numbers')
    if state=='verified' and (source is None or tuple(source)!=tuple(displayed)):raise ValueError('verified claim requires matching source')
    return {'genre':genre,'state':state,'displayed':list(displayed),'source':list(source) if source else None,'human_review_required':True,'publication_approved':False}
def validate_layout():
    return X>=24 and Y>=125 and X+W<=1040 and Y+H<645 and END>START and END<23.04
def render_badge(path):
    if not validate_layout():raise ValueError('unsafe layout')
    from PIL import Image,ImageDraw,ImageFont
    im=Image.new('RGBA',(W,H),(0,0,0,0));d=ImageDraw.Draw(im)
    d.rounded_rectangle((1,1,W-2,H-2),radius=25,fill=(2,23,42,248),outline=(255,186,72,255),width=4)
    font='/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc'
    regular='/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc'
    if not Path(font).exists():raise RuntimeError('Noto Japanese font required')
    bold=ImageFont.truetype(font,64);medium=ImageFont.truetype(font,46)
    small=ImageFont.truetype(regular,34);mini=ImageFont.truetype(font,27)
    d.text((47,24),'STEP 03  /  BEFORE CHECK',font=mini,fill=(99,221,226,255))
    d.text((44,86),'仮集計を見える化',font=bold,fill=(255,250,243,255))
    d.rounded_rectangle((46,207,244,275),radius=18,fill=(255,186,72,255))
    d.text((76,217),'検証前',font=medium,fill=(8,31,45,255))
    d.text((274,216),'数値は要確認',font=medium,fill=(255,219,156,255))
    d.text((47,317),'3か月分の架空データを比較',font=small,fill=(222,242,245,255))
    d.text((47,372),'この後、元データと照合・修正します',font=small,fill=(222,242,245,255))
    d.rounded_rectangle((46,447,487,486),radius=11,fill=(16,76,93,255))
    d.text((62,448),'架空データ / デモ映像',font=mini,fill=(218,244,246,255))
    Path(path).parent.mkdir(parents=True,exist_ok=True);im.save(path)
def render(source,badge,output):
    source,badge,output=map(Path,(source,badge,output))
    if not source.is_file() or not badge.is_file() or source.resolve()==output.resolve():raise ValueError('missing source or unsafe output')
    vf=("[1:v]format=rgba,fade=t=in:st=5.667:d=0.18:alpha=1,"
        "fade=t=out:st=8.20:d=0.16:alpha=1[proof];"
        "[0:v][proof]overlay=x=30:y=130:format=auto:enable='between(t,5.667,8.367)'[v]")
    cmd=['ffmpeg','-y','-hide_banner','-loglevel','error','-i',str(source),'-loop','1','-framerate','30','-i',str(badge),'-filter_complex',vf,'-map','[v]','-map','0:a:0','-c:v','libx264','-preset','veryfast','-crf','18','-pix_fmt','yuv420p','-c:a','copy','-movflags','+faststart','-t','23.033333',str(output)]
    subprocess.run(cmd,check=True);return cmd
def main():
    p=argparse.ArgumentParser();p.add_argument('--source',type=Path,required=True);p.add_argument('--badge',type=Path,required=True);p.add_argument('--output',type=Path,required=True)
    a=p.parse_args()
    before=sum_evidence([(12,8),(16,9),(17,11)]);after=sum_evidence([(12,8),(16,9),(18,12)])
    assert before==(45,28) and after==(46,29)
    proof=validate_proof(genre='ai_work',state='provisional',displayed=before,source=after)
    render_badge(a.badge);cmd=render(a.source,a.badge,a.output)
    print(json.dumps({'policy':POLICY,'proof':proof,'command':cmd,'fictional':True},ensure_ascii=False))
if __name__=='__main__':main()
