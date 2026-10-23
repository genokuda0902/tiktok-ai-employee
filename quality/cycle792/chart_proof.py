"""cycle792: local review-only 4-month chart proof overlay.
Original user media and voice remain local; CI uses a synthetic tone fixture.
This is a reimplementation, NOT recovered v33 source.
"""
import argparse,hashlib,json,subprocess
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
GENRES=('ai_productivity','finance','career','business','education','lifestyle','science','travel','health','entertainment')
W,H,FPS=1080,1920,30
START,END=9.,11.
FONT='/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc'
BOLD='/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc'

def validate(c):
    if c.get('mode')!='review_only' or c.get('publication_approved') is not False or c.get('rights_reviewed') is not False: raise ValueError('FAIL CLOSED: approval required')
    if c.get('genre') not in GENRES or c.get('canvas')!=[W,H] or c.get('fps')!=FPS or abs(c.get('duration_seconds',0)-23.843)>.005: raise ValueError('bad format')
    if c.get('source_data_kind')!='synthetic': raise ValueError('data must be synthetic')
    v=c.get('values_man_yen')
    if not isinstance(v,list) or len(v)!=4 or any(type(x) is not int or x<0 or x>100 for x in v):raise ValueError('four integer values required')
    if sum(v)!=c.get('total_man_yen') or c.get('months')!=['1月','2月','3月','4月']:raise ValueError('data inconsistency')
    return True

def font(sz,bold=False):return ImageFont.truetype(BOLD if bold else FONT,sz)
def ease(p):
    p=max(0,min(1,p));return 1-(1-p)**3

def bar_geometry(c,p):
    validate(c);v=c['values_man_yen']
    return [{'month':m,'value':x,'x':155+i*166,'y_bottom':1105,'height':int(300*x/max(1,max(v))*ease((p-i*.17)/.42))} for i,(m,x) in enumerate(zip(c['months'],v))]

def frame(c,p):
    validate(c)
    im=Image.new('RGBA',(W,H),(0,0,0,0));d=ImageDraw.Draw(im)
    d.rounded_rectangle((58,520,870,1300),radius=33,fill=(247,251,254,255),outline=(47,186,199,255),width=5)
    d.text((98,566),'4か月の売上比較',font=font(52,True),fill=(16,39,58,255))
    d.text((98,648),'架空データ  |  単位：万円',font=font(29),fill=(60,91,112,255))
    d.rounded_rectangle((574,643,824,715),radius=18,fill=(14,69,86,255))
    d.text((600,655),f"合計 {c['total_man_yen']}万円",font=font(34,True),fill='white')
    for value in (0,10,20):
        y=1105-round(300*value/20)
        d.line((130,y,824,y),fill=(189,209,220,255),width=2)
        d.text((90,y-20),str(value),font=font(26),fill=(78,104,122,255))
    for b in bar_geometry(c,p):
        x,y,v=b['x'],1105-b['height'],b['value']
        if b['height']>0:
            d.rounded_rectangle((x,y,x+98,1105),radius=14,fill=(22,155,192,255))
            d.rectangle((x,1091,x+98,1105),fill=(22,155,192,255))
        if b['height']>=int(300*v/20*.82):
            s=f'{v}万';bb=d.textbbox((0,0),s,font=font(35,True))
            d.text((x+49-(bb[2]-bb[0])/2,y-55),s,font=font(35,True),fill=(16,57,72,255))
        d.text((x+15,1131),b['month'],font=font(33,True),fill=(24,48,67,255))
    d.rounded_rectangle((206,1212,726,1281),radius=15,fill=(5,20,30,255))
    d.text((226,1221),'グラフで売上の推移を確認',font=font(36,True),fill='white')
    # Cover the ENTIRE inherited chart card; a smaller inset leaves ghost bars.
    card=im.crop((58,520,871,1301)).resize((944,913),Image.Resampling.LANCZOS)
    out=Image.new('RGBA',(W,H),(0,0,0,0));out.alpha_composite(card,(68,603))
    return out

def cmd(args):
    p=subprocess.run(args,capture_output=True,text=True)
    if p.returncode:raise RuntimeError('command failed: '+' '.join(map(str,args))+'\n'+p.stderr[-2500:])
    return p

def verify(path,duration):
    data=json.loads(cmd(['ffprobe','-v','error','-show_entries','stream=codec_type,codec_name,width,height,r_frame_rate,nb_frames:format=duration','-of','json',str(path)]).stdout)
    v=next(x for x in data['streams'] if x['codec_type']=='video');a=next(x for x in data['streams'] if x['codec_type']=='audio')
    if (v['codec_name'],v['width'],v['height'],v['r_frame_rate'],a['codec_name'])!=('h264',W,H,'30/1','aac'):raise ValueError('bad codec or dimensions')
    if abs(float(data['format']['duration'])-duration)>.08:raise ValueError('bad duration')
    cmd(['ffmpeg','-v','error','-xerror','-i',str(path),'-f','null','-'])
    return {'duration':float(data['format']['duration']),'frames':int(v.get('nb_frames') or 0),'width':W,'height':H,'fps':FPS,'video':'h264','audio':'aac','full_decode':'PASS'}

def make_frames(c,folder):
    folder=Path(folder);folder.mkdir(parents=True,exist_ok=True)
    n=round((END-START)*FPS)
    for i in range(n):frame(c,i/(n-1)).save(folder/f'chart_{i:03d}.png',compress_level=2)
    return n

def render(c,source,output,frames_dir,fixture=False):
    validate(c);source=Path(source);output=Path(output);output.parent.mkdir(parents=True,exist_ok=True)
    if not source.is_file():raise FileNotFoundError(source)
    n=make_frames(c,frames_dir)
    graph=f"[1:v]format=rgba,setpts=PTS-STARTPTS+{START}/TB[chart];[0:v][chart]overlay=0:0:format=auto:shortest=0:eof_action=pass:enable='between(t,{START},{END})'[v]"
    cmd(['ffmpeg','-hide_banner','-loglevel','error','-y','-i',str(source),'-framerate',str(FPS),'-i',str(Path(frames_dir)/'chart_%03d.png'),'-filter_complex',graph,'-map','[v]','-map','0:a:0','-c:v','libx264','-preset','ultrafast' if fixture else 'veryfast','-crf','31' if fixture else '19','-pix_fmt','yuv420p','-c:a','copy','-movflags','+faststart',str(output)])
    r=verify(output,c['duration_seconds'])
    r.update({'cycle':792,'genre':c['genre'],'source_kind':'synthetic_fixture' if fixture else 'local_inherited_user_media','synthetic_chart_values':c['values_man_yen'],'chart_total':c['total_man_yen'],'chart_frames':n,'chart_interval':[START,END],'voice_transcript_verified':False,'semantic_caption_sync_verified':False,'rights_reviewed':False,'publication_approved':False,'status':'HUMAN_REVIEW','sha256':hashlib.sha256(output.read_bytes()).hexdigest()})
    return r

def main():
    p=argparse.ArgumentParser()
    for x in ('config','output','frames','report'):p.add_argument('--'+x,required=True)
    p.add_argument('--input');p.add_argument('--synthetic-ci-fixture',action='store_true')
    a=p.parse_args();c=json.loads(Path(a.config).read_text(encoding='utf-8'));validate(c)
    if a.synthetic_ci_fixture:
        if '_SYNTHETIC_TONE_' not in a.output:raise ValueError('synthetic output label required')
        source=Path(a.frames).parent/'synthetic_input.mp4';source.parent.mkdir(parents=True,exist_ok=True)
        cmd(['ffmpeg','-hide_banner','-loglevel','error','-y','-f','lavfi','-i',f"color=c=0x062137:s=1080x1920:r=30:d={c['duration_seconds']}",'-f','lavfi','-i',f"sine=frequency=392:sample_rate=48000:duration={c['duration_seconds']}",'-c:v','libx264','-preset','ultrafast','-crf','32','-pix_fmt','yuv420p','-c:a','aac','-b:a','64k','-shortest',str(source)])
    else:
        if not a.input or '_REVIEW_ONLY' not in a.output:raise ValueError('local input and review-only output required')
        source=Path(a.input)
    r=render(c,source,a.output,a.frames,fixture=a.synthetic_ci_fixture)
    Path(a.report).parent.mkdir(parents=True,exist_ok=True)
    Path(a.report).write_text(json.dumps(r,ensure_ascii=False,indent=2),encoding='utf-8')
    print(json.dumps(r,ensure_ascii=False))
if __name__=='__main__':main()
