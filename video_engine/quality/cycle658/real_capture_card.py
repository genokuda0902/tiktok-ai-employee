"""Reusable safe-framed real application screenshot cards (local-only assets).

The screenshot is evidence of an app state, NOT evidence of continuous operation.
Unapproved screenshot assets must never be committed, uploaded, or published.
"""
from __future__ import annotations
import csv
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageOps

FONT='/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc'
TABLE_RECT=(85,378,335,585)
FORMULA_RECT=(320,161,640,191)
CHART_RECT=(204,369,1075,790)

def synthetic_csv_evidence(path: str | Path, expected=(120,150,200,180)) -> tuple[int,...]:
    """Read the original synthetic source; fail closed on any changed value."""
    with open(path, encoding='utf-8-sig', newline='') as fh:
        rows=list(csv.reader(fh))
    if len(rows)!=6 or rows[0]!=['月','売上（千円）']:
        raise ValueError('CSV schema changed')
    values=[]
    for i,row in enumerate(rows[1:5],start=1):
        if len(row)!=2 or row[0]!=f'{i}月' or not row[1].isdigit():
            raise ValueError(f'Invalid source data row {i}')
        values.append(int(row[1]))
    if rows[5]!=['合計','=SUM(B2:B5)'] or tuple(values)!=tuple(expected) or sum(values)!=650:
        raise ValueError('CSV and on-screen numeric proof are inconsistent')
    return tuple(values)

def crop_evidence(img:Image.Image, box:tuple[int,int,int,int]) -> Image.Image:
    if len(box)!=4 or not (0<=box[0]<box[2]<=img.width and 0<=box[1]<box[3]<=img.height):
        raise ValueError('Crop outside screenshot: evidence invalid')
    return img.crop(box)

def safe_real_capture_card(canvas:Image.Image, *, screenshot:Image.Image, mode:str,
                           progress:float=1.0, top:int=244, font_path:str=FONT) -> dict:
    """Composite sanitized actual Calc state; no source warning bars in selected crops.

    This function does not make claims about actual operation recordings, efficiency
    gains, or unverified model output. The underlying source must be local synthetic.
    """
    if mode not in ('table','chart'):
        raise ValueError('Unsupported evidence mode')
    if screenshot.size!=(1440,900):
        raise ValueError('Unexpected screenshot size: crop evidence must be re-reviewed')
    p=max(0,min(1,float(progress)))
    d=ImageDraw.Draw(canvas)
    x0,x1=43,497
    d.rounded_rectangle((x0,top,x1,top+444),radius=22,fill='#f7fbff')
    d.rounded_rectangle((x0,top,x1,top+51),radius=20,fill='#115c84')
    font=ImageFont.truetype(font_path,21)
    d.text((x0+17,top+10),'Calc実画面｜架空データ・静止画',font=font,fill='white')
    if mode=='table':
        region=crop_evidence(screenshot,TABLE_RECT)
        region=ImageOps.fit(region,(410,315),Image.Resampling.LANCZOS,centering=(.45,.53))
        canvas.paste(region,(x0+22,top+63))
        formula=crop_evidence(screenshot,FORMULA_RECT)
        formula=ImageOps.fit(formula,(393,35),Image.Resampling.LANCZOS)
        canvas.paste(formula,(x0+30,top+365))
        y=top+63+int(315*.85)
        d=ImageDraw.Draw(canvas)
        d.rounded_rectangle((x0+20,y,x0+434,y+40),radius=7,outline='#00b8c6',width=3)
    else:
        region=crop_evidence(screenshot,CHART_RECT)
        region=region.resize((420,322),Image.Resampling.LANCZOS)
        canvas.paste(region,(x0+17,top+61))
        d=ImageDraw.Draw(canvas)
        labels=('1月','2月','3月','4月')
        for i,month in enumerate(labels):
            d.text((x0+44+i*100,top+383),month,font=ImageFont.truetype(font_path,17),fill='#1a506d')
        cue_x=x0+17+int(410*p)
        d.rounded_rectangle((cue_x,top+52,cue_x+4,top+61),radius=2,fill='#00b8c6')
    return {'source':'REAL_CALC_SCREENSHOT','synthetic':True,'continuous_operation':False,
            'screenshot_review_required':True,'mode':mode,'rights_approved':False}
