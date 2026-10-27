"""cycle890: review-only Japanese prompt typing animation for ten genres.

Synthetic offline UI, NOT actual ChatGPT/Excel capture. Never publish or upload
inherited media. Use an explicitly SHA-pinned local input.
"""
import argparse, hashlib, json, re, subprocess
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

FPS=30; START=251; END=336; FRAMES=691
OVERLAY_Y=940; PATCH_HEIGHT=208
FONT='/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc'
GENRES=('ai_productivity','beauty','romance_psychology','money_saving','sales_business',
'career','health_lifestyle','trivia_science','travel_food','product_lifestyle')
PROMPTS={
'ai_productivity':('この3期間の架空データを整理','2項目の合計とグラフを作成','最後に元データと照合して'),
'beauty':('架空の美容記録を整理して','項目ごとの変化を表にして','元の記録と照合して'),
'romance_psychology':('架空の会話メモを整理して','発言と状況を区別してまとめ','元のメモと照合して'),
'money_saving':('架空の支出記録を整理して','費目別の合計を計算して','元の金額と照合して'),
'sales_business':('架空の営業記録を整理して','月別の件数を集計して','元の件数と照合して'),
'career':('架空の業務記録を整理して','担当別に進捗をまとめて','元の記録と照合して'),
'health_lifestyle':('架空の生活記録を整理して','日付別の傾向を表にして','元の記録と照合して'),
'trivia_science':('架空の観測記録を整理して','項目別の数値を表にして','元の記録と照合して'),
'travel_food':('架空の旅程メモを整理して','日付別の予定を表にして','元の旅程と照合して'),
'product_lifestyle':('架空の商品比較表を整理して','仕様と価格を分けてまとめ','元の表と照合して')}
POLICY={'review_only':True,'publication_approved':False,'external_upload':False,
'automatic_posting':False,'source_rights_reviewed':False,'fictional_data':True}

def sha256(path):
    h=hashlib.sha256()
    with open(path,'rb') as f:
        for b in iter(lambda:f.read(1024*1024),b''):h.update(b)
    return h.hexdigest()

def validate_prompt(lines):
    if not isinstance(lines,(list,tuple)) or len(lines)!=3:raise ValueError('three lines required')
    for s in lines:
        if not isinstance(s,str) or not 1<=len(s)<=32:raise ValueError('unsafe length')
        if re.search(r'https?://|www\.|@|[<>\r\n]|\d{3}[- ]?\d{4}|\d{11}',s,re.I):
            raise ValueError('possible identifier')
    return True

def validate_manifest(manifest,source):
    if any(manifest.get(k)!=v for k,v in POLICY.items()):raise ValueError('review policy mismatch')
    if manifest.get('source_sha256')!=sha256(source):raise ValueError('source hash mismatch')
    return True

def char_count(frame,lines):
    if not 0<=frame<END-START:raise ValueError('outside scene')
    return min(sum(map(len,lines)),frame*sum(map(len,lines))//73)

def visible_lines(frame,lines):
    validate_prompt(lines)
    remaining=char_count(frame,lines);out=[]
    for s in lines:
        n=min(len(s),remaining);out.append(s[:n]);remaining-=n
    return tuple(out)

def safe_geometry():
    return OVERLAY_Y>245 and OVERLAY_Y+PATCH_HEIGHT<1240<1438

def draw_patch(frame,genre='ai_productivity'):
    if genre not in GENRES:raise ValueError('unknown genre')
    lines=PROMPTS[genre];validate_prompt(lines)
    if not safe_geometry():raise ValueError('unsafe geometry')
    im=Image.new('RGBA',(1080,PATCH_HEIGHT),(0,0,0,0))
    d=ImageDraw.Draw(im,'RGBA')
    d.rounded_rectangle((84,0,1031,207),radius=18,fill=(229,240,246,255))
    font=ImageFont.truetype(FONT,41,index=0)
    visible=visible_lines(frame,lines)
    for i,(y,s) in enumerate(zip((22,83,144),visible)):
        if not s:continue
        if i==2 and frame>=58:
            d.rounded_rectangle((104,y-2,1015,y+53),radius=9,fill=(205,234,241,255))
        d.text((115,y),s,font=font,fill=(14,39,56,255))
        if d.textbbox((0,0),s,font=font)[2]>881:raise ValueError('text overflow')
    if frame%14<10 and frame<END-START-4:
        i=next((i for i,s in enumerate(visible) if len(s)<len(lines[i])),2)
        s=visible[i];w=d.textbbox((0,0),s,font=font)[2] if s else 0
        x=116+w
        if x<1015:d.rounded_rectangle((x,(22,83,144)[i]+5,x+5,(22,83,144)[i]+44),
                                    radius=2,fill=(11,148,189,255))
    return im

def probe(path):
    return json.loads(subprocess.check_output(['ffprobe','-v','error','-show_entries',
    'format=duration:stream=codec_type,codec_name,width,height,r_frame_rate,nb_frames,sample_rate,channels',
    '-of','json',str(path)],text=True))

def render(source,output,manifest,work,report):
    source=Path(source);output=Path(output);work=Path(work);report=Path(report)
    validate_manifest(json.loads(Path(manifest).read_text()),source)
    m=probe(source)
    v=next(x for x in m['streams'] if x['codec_type']=='video')
    a=next(x for x in m['streams'] if x['codec_type']=='audio')
    if (v['codec_name'],v['width'],v['height'],v['r_frame_rate'],int(v['nb_frames']))!=('h264',1080,1920,'30/1',FRAMES):
        raise ValueError('unexpected video')
    if (a['codec_name'],int(a['sample_rate']),a['channels'])!=('aac',48000,2):
        raise ValueError('unexpected audio')
    work.mkdir(parents=True,exist_ok=True)
    for i in range(END-START):draw_patch(i).save(work/f'{i:03d}.png',compress_level=2)
    output.parent.mkdir(parents=True,exist_ok=True)
    filt=(f'[1:v]format=rgba,setpts=PTS+{START}/({FPS}*TB)[ov];'
        f"[0:v][ov]overlay=0:{OVERLAY_Y}:shortest=0:repeatlast=0:eof_action=pass:format=auto:enable='between(n,{START},{END-1})'[v]")
    subprocess.run(['ffmpeg','-hide_banner','-loglevel','error','-y','-i',str(source),
        '-framerate','30','-start_number','0','-i',str(work/'%03d.png'),
        '-filter_complex',filt,'-map','[v]','-map','0:a:0','-frames:v',str(FRAMES),
        '-c:v','libx264','-preset','veryfast','-crf','19','-pix_fmt','yuv420p',
        '-c:a','copy','-movflags','+faststart',str(output)],check=True,timeout=300)
    subprocess.run(['ffmpeg','-v','error','-xerror','-i',str(output),
        '-map','0:v:0','-map','0:a:0','-f','null','-'],check=True,timeout=120)
    result={'cycle':890,'source_sha256':sha256(source),'output_sha256':sha256(output),
        'changed_frames':[START,END-1],'full_av_decode':'PASS','audio_elementary':'COPY',
        'japanese_transcript_semantics':'UNVERIFIED','publication':'NOT_APPROVED'}
    report.write_text(json.dumps(result,ensure_ascii=False,indent=2))
    return result

if __name__=='__main__':
    p=argparse.ArgumentParser()
    for n in ('source','output','manifest','work','report'):p.add_argument('--'+n,required=True)
    a=p.parse_args()
    print(json.dumps(render(a.source,a.output,a.manifest,a.work,a.report),ensure_ascii=False))
