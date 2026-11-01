"""Cycle1112: two-beat numeric verification insert, REVIEW ONLY.

Works on local SHA-pinned review media. No network, publication, private media
commit, external asset download or speech/caption semantic approval.
"""
from __future__ import annotations
import argparse
import hashlib
import json
import subprocess
import tempfile
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

GENRES = ('ai_work','money','career','business','health','study','lifestyle','technology','travel','mindset')
ACCENTS = dict(zip(GENRES, ('#33d6ce','#6bd6ad','#82cfff','#54d7c7','#89d8b5','#7bd8ef','#75d6cc','#69d5ff','#87dcc9','#a0caff')))
FONT = '/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc'
FONT_REG = '/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc'
CANVAS = (1080,1920)
SAFE_BOTTOM = 1080
CUT = (11.70,12.50,13.29)
REQUIRED = {'genre','review_only','rights_status','contains_private_data','synthetic_scenario','label','input_a','input_b','expected_total'}

def sha(path):
    h=hashlib.sha256()
    with open(path,'rb') as f:
        for chunk in iter(lambda:f.read(1024*1024),b''): h.update(chunk)
    return h.hexdigest()

def run(cmd):
    p=subprocess.run(cmd,capture_output=True,text=True)
    if p.returncode: raise RuntimeError('command failed: '+str(cmd[:4])+' '+p.stderr[-2000:])
    return p.stdout

def probe(path):
    return json.loads(run(['ffprobe','-v','error','-show_streams','-show_format','-of','json',str(path)]))

def audio_sha(path):
    with tempfile.TemporaryDirectory() as td:
        out=Path(td)/'a.aac'
        run(['ffmpeg','-v','error','-y','-i',str(path),'-map','0:a:0','-c:a','copy','-f','adts',str(out)])
        return sha(out)

def validate(m):
    if set(m)!=REQUIRED: raise ValueError('manifest schema mismatch')
    if m['genre'] not in GENRES: raise ValueError('genre not approved')
    if m['review_only'] is not True or m['rights_status']!='unverified' or m['contains_private_data'] is not False or m['synthetic_scenario'] is not True:
        raise ValueError('fail-closed privacy/rights/publication gate')
    if not isinstance(m['label'],str) or not 1<=len(m['label'])<=8 or any(ord(c)<32 for c in m['label']):
        raise ValueError('unsafe label')
    for k in ('input_a','input_b','expected_total'):
        if type(m[k]) is not int or not 0<=m[k]<=999: raise ValueError('unsafe numeric input '+k)
    if m['input_a']+m['input_b']!=m['expected_total']:
        raise ValueError('false arithmetic proof')
    if not 0<=CUT[0]<CUT[1]<CUT[2]<=23.03334: raise ValueError('invalid timeline')
    return m

def image_for(m,stage,path):
    validate(m)
    if stage not in (1,2): raise ValueError('stage')
    im=Image.new('RGBA',CANVAS,(0,0,0,0));d=ImageDraw.Draw(im)
    accent=ACCENTS[m['genre']]
    # Main proof insert: replaces only scene05 content, never narration/caption area.
    rect=(58,315,1022,1025)
    assert rect[3]<SAFE_BOTTOM
    d.rounded_rectangle(rect, radius=30, fill=(4,20,39,251),outline=accent,width=5)
    d.rounded_rectangle((84,345,476,412),radius=15,fill=accent)
    d.text((109,355),'数字を1行ずつ検算',font=ImageFont.truetype(FONT,36),fill='#001922')
    d.text((91,458),f'{m["label"]} の元データ',font=ImageFont.truetype(FONT,48),fill='#e5f7ff')
    d.rounded_rectangle((90,545,989,700),radius=18,fill=(12,53,75,255))
    d.text((121,563),f'営業A {m["input_a"]}  ＋  営業B {m["input_b"]}',font=ImageFont.truetype(FONT,48),fill='white')
    if stage==1:
        d.text((118,759),'STEP 1   元データを照合',font=ImageFont.truetype(FONT,47),fill=accent)
        d.text((118,849),'合計はまだ未確認',font=ImageFont.truetype(FONT,39),fill='#e5f7ff')
    else:
        d.text((118,737),f'=  {m["expected_total"]}',font=ImageFont.truetype(FONT,91),fill='#f5d86b')
        d.rounded_rectangle((544,752,964,844),radius=22,fill=accent)
        d.text((582,766),'検算 OK',font=ImageFont.truetype(FONT,48),fill='#00202a')
        d.text((118,888),'STEP 2   足し算を再確認',font=ImageFont.truetype(FONT,40),fill='#d8f4f6')
    d.text((102,965),'架空の数字・結果を保証するものではありません',font=ImageFont.truetype(FONT_REG,24),fill='#b6c9d1')
    im.save(path)
    return path

def render(source,out,source_sha,m,times=CUT):
    validate(m)
    if sha(source)!=source_sha: raise ValueError('source SHA mismatch')
    p=probe(source)
    v=next((x for x in p['streams'] if x['codec_type']=='video'),None)
    a=next((x for x in p['streams'] if x['codec_type']=='audio'),None)
    if not v or (v['codec_name'],v['width'],v['height'],v['r_frame_rate'])!=('h264',1080,1920,'30/1'):
        raise ValueError('unsupported source video')
    if not a or (a['codec_name'],a['sample_rate'])!=('aac','48000'):
        raise ValueError('unsupported source audio')
    t1,t2,t3=times
    if not (11.2<=t1<t2<t3<=13.8 and .4<=t2-t1<=1.2 and .4<=t3-t2<=1.2):
        raise ValueError('unsafe edit timing')
    out=Path(out);out.parent.mkdir(parents=True,exist_ok=True)
    with tempfile.TemporaryDirectory() as td:
        first=image_for(m,1,Path(td)/'stage1.png')
        second=image_for(m,2,Path(td)/'stage2.png')
        fc=(f"[0:v][1:v]overlay=0:0:enable='gte(t,{t1})*lt(t,{t2})':eof_action=pass[x];"
            f"[x][2:v]overlay=0:0:enable='gte(t,{t2})*lt(t,{t3})':eof_action=pass[v]")
        run(['ffmpeg','-hide_banner','-loglevel','error','-y','-i',str(source),'-loop','1','-i',str(first),'-loop','1','-i',str(second),'-filter_complex',fc,'-map','[v]','-map','0:a:0','-c:v','libx264','-preset','veryfast','-crf','18','-pix_fmt','yuv420p','-c:a','copy','-frames:v',str(int(v['nb_frames'])),'-movflags','+faststart',str(out)])
    q=probe(out); vv=next(x for x in q['streams'] if x['codec_type']=='video')
    return {'source_sha256':source_sha,'output_sha256':sha(out),'changed_seconds':list(times),
            'duration':float(q['format']['duration']),'frames':int(vv['nb_frames']),
            'size':[vv['width'],vv['height']],'audio_bitstream_identical':audio_sha(source)==audio_sha(out),
            'arithmetic':f'{m["input_a"]}+{m["input_b"]}={m["expected_total"]}',
            'review_only':True,'publication':'NOT_APPROVED','speech_caption_semantics':'UNVERIFIED'}

def main():
    p=argparse.ArgumentParser()
    for k in ('source','source-sha','manifest','out','report'): p.add_argument('--'+k,required=True)
    a=p.parse_args()
    m=json.loads(Path(a.manifest).read_text(encoding='utf8'))
    result=render(a.source,a.out,a.source_sha,m)
    Path(a.report).write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf8')
    print(json.dumps(result,ensure_ascii=False))
if __name__=='__main__': main()
