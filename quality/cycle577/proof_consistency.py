#!/usr/bin/env python3
"""Cycle577: repair inconsistent cross-scene proof labels (review-only).
Requires cycle576's SHA-locked MP4. No inherited media is licensed for posting.
"""
import argparse, hashlib, json, subprocess
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

SOURCE_SHA = 'f62d87afcb46c92a97434740293f65b02aa2e3225493225d505b57ac30fb911b'
GENRES = ('ai_productivity','beauty','relationships','finance','sales','career','wellness','science','travel_food','product_comparison')
DATA = (120,150,200,250)
FONT = '/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc'

def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()

def validate_proof(values, cell_range, expected, genre):
    if genre not in GENRES: raise ValueError('unknown genre')
    if len(values)!=4 or any(type(v)!=int or v<0 for v in values): raise ValueError('invalid synthetic data')
    if cell_range!='B2:B5': raise ValueError('range differs from source data scene')
    if sum(values)!=expected: raise ValueError('calculation does not match evidence')
    return True

def make_overlay(path, values=DATA):
    validate_proof(values,'B2:B5',720,'ai_productivity')
    im=Image.new('RGBA',(1080,1920),(0,0,0,0))
    d=ImageDraw.Draw(im)
    # Only replace the contradictory arithmetic/formula regions of the comparison scene.
    d.rounded_rectangle((100,1210,526,1426),radius=22,fill=(28,26,42,255))
    d.text((122,1250),'120 + 150 +',font=ImageFont.truetype(FONT,45),fill='white')
    d.text((122,1330),'200 + 250 = 720',font=ImageFont.truetype(FONT,38),fill='#ffced5')
    d.rounded_rectangle((570,1235,986,1410),radius=22,fill=(9,43,45,255),outline=(93,232,209,255),width=3)
    d.text((587,1272),'=SUM(B2:B5)',font=ImageFont.truetype(FONT,49),fill='#e7fff9')
    d.text((590,1340),'4件の合計 = 720',font=ImageFont.truetype(FONT,33),fill='#82f3df')
    # The visible cell labels must match the earlier B2:B5 selection, not A1:A4.
    for label,top in zip(('B2','B3','B4','B5'),(814,916,1018,1120)):
        d.rounded_rectangle((598,top,691,top+74),radius=10,fill=(229,242,242,255))
        d.text((615,top+8),label,font=ImageFont.truetype(FONT,43),fill=(31,64,74,255))
    im.save(path)

def run(source, output, genre='ai_productivity'):
    validate_proof(DATA,'B2:B5',720,genre)
    if genre!='ai_productivity': raise ValueError('other genres need separately approved source')
    source,output=Path(source),Path(output)
    if sha(source)!=SOURCE_SHA: raise ValueError('source SHA mismatch')
    output.parent.mkdir(parents=True,exist_ok=True)
    overlay=output.parent/'proof_overlay.png'
    make_overlay(overlay)
    cmd=['ffmpeg','-hide_banner','-loglevel','error','-y','-i',str(source),'-loop','1','-i',str(overlay),
         '-filter_complex','[0:v][1:v]overlay=0:0:enable=between(t\\,16.95\\,18.45):shortest=1,format=yuv420p[v]',
         '-map','[v]','-map','0:a:0','-map','0:s:0','-c:v','libx264','-preset','ultrafast','-crf','19',
         '-r','30','-c:a','copy','-c:s','mov_text','-t','20','-movflags','+faststart',str(output)]
    p=subprocess.run(cmd,capture_output=True,text=True)
    if p.returncode: raise RuntimeError(p.stderr[-3000:])
    report={'cycle':577,'source_sha256':SOURCE_SHA,'output_sha256':sha(output),
            'proof':{'values':DATA,'cell_range':'B2:B5','sum':720},
            'changed_seconds':[16.95,18.45],'genre':genre,
            'japanese_narration':'ABSENT','semantic_sync':'UNVERIFIED',
            'rights':'INHERITED_ASSETS_UNVERIFIED','human_review':'REQUIRED',
            'publication':'NOT_APPROVED','cost_jpy':0}
    (output.parent/'qa.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
    return report

if __name__=='__main__':
    ap=argparse.ArgumentParser()
    ap.add_argument('--source',required=True)
    ap.add_argument('--output',required=True)
    ap.add_argument('--genre',default='ai_productivity')
    a=ap.parse_args()
    print(json.dumps(run(a.source,a.output,a.genre),ensure_ascii=False,indent=2))
