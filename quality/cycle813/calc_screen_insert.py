#!/usr/bin/env python3
"""Insert a local Calc screen recording into a private review MP4.

Ten-genre compositing component, NOT recovered v33 code. CI uses synthetic
test footage; inherited Japanese narration and actual GUI footage stay local.
No upload, TikTok posting or automatic publication.
"""
from __future__ import annotations
import argparse
import hashlib
import json
import os
from pathlib import Path
import subprocess
import tempfile
from PIL import Image, ImageDraw, ImageFont

W, H, FPS, TOTAL = 1080, 1920, 30, 718
START, DURATION = 90, 90
CARD_X, CARD_Y, CARD_W, CARD_H = 115, 690, 850, 600
GENRE_ACCENTS = {
    'ai_work':'#55d6ff', 'beauty':'#ff99d4',
    'love_psychology':'#ff9cbb', 'money_saving':'#8fe7a2',
    'sales_business':'#60e6d2', 'career':'#a8b8ff',
    'health_life':'#93e2b2', 'science':'#9ecbff',
    'travel_food':'#ffcc83', 'product_life':'#a8d8ef',
}
AUTO_POST = False
PUBLICATION_APPROVED = False
FONT_CANDIDATES = (
    '/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc',
    '/usr/share/fonts/truetype/noto/NotoSansCJK-Bold.ttc',
)

def font(size):
    path = os.environ.get('CYCLE813_FONT') or next((p for p in FONT_CANDIDATES if Path(p).is_file()), None)
    if not path: raise RuntimeError('Japanese font unavailable; set CYCLE813_FONT')
    return ImageFont.truetype(path, size)

def run(cmd):
    p = subprocess.run([str(x) for x in cmd], capture_output=True, text=True)
    if p.returncode:
        raise RuntimeError(f"exit={p.returncode}: {' '.join(map(str,cmd))}\n{p.stderr[-2500:]}")
    return p.stdout

def probe(path):
    return json.loads(run(['ffprobe','-v','error','-show_streams','-show_format','-of','json',path]))

def sha(path):
    h=hashlib.sha256()
    with open(path,'rb') as f:
        for part in iter(lambda:f.read(1024*1024),b''): h.update(part)
    return h.hexdigest()

def audio_sha(path):
    with tempfile.TemporaryDirectory() as td:
        out=Path(td)/'audio.aac'
        run(['ffmpeg','-v','error','-y','-i',path,'-map','0:a:0','-c:a','copy','-f','adts',out])
        return sha(out)

def validate(genre, target, actual, fictional_data):
    if genre not in GENRE_ACCENTS: raise ValueError('Unknown genre')
    if not fictional_data: raise ValueError('Only explicitly fictional/sanitized fixture data allowed')
    if not (0 <= actual <= target <= 999): raise ValueError('Invalid nonnegative target/actual')
    if CARD_X < 100 or CARD_X+CARD_W > W-100: raise ValueError('Card not horizontally safe')
    if CARD_Y < 620 or CARD_Y+CARD_H > 1320: raise ValueError('Card overlaps bottom subtitles')
    return GENRE_ACCENTS[genre]

def source_index(i, count):
    """Select 90 monotonically increasing capture frames, leaving margins."""
    if not 0 <= i < DURATION or count < 90: raise ValueError('Insufficient capture frames')
    return round((count-1) * (0.06 + 0.92*i/(DURATION-1)))

def draw_card(i, screenshot, genre, target, actual, synthetic_capture=False):
    if not 0 <= i < DURATION: raise ValueError('Outside demo segment')
    accent=GENRE_ACCENTS[genre]
    card=Image.new('RGB',(CARD_W,CARD_H),'#061b2b')
    d=ImageDraw.Draw(card)
    d.rounded_rectangle((4,4,CARD_W-5,CARD_H-5),radius=30,fill='#0b2538',outline=accent,width=3)
    d.text((30,28),'LIVE SCREEN / CALC',font=font(33),fill='#f0fbff')
    d.rounded_rectangle((585,26,823,79),radius=18,fill='#234451')
    tag='検証用素材' if synthetic_capture else '架空データ・実操作'
    d.text((600,36),tag,font=font(25),fill='#fff0a7')
    # Opaque screen content prevents ghosting from the replaced fake UI.
    screen=screenshot.convert('RGB').resize((800,292),Image.Resampling.LANCZOS)
    card.paste(screen,(25,105))
    d.rounded_rectangle((24,104,826,398),radius=7,outline='#a9d3dc',width=3)
    d.text((35,425),'目標を数値にする',font=font(33),fill='#bce3ef')
    d.text((35,478),'成約目標',font=font(35),fill='#ffffff')
    shown='入力中…' if i<29 else f'{target} 件'
    d.text((352,463),shown,font=font(59 if i>=29 else 39),fill=accent)
    if i>=69:
        d.rounded_rectangle((605,466,813,544),radius=18,fill='#185667')
        d.text((621,484),f'差分 {target-actual} 件',font=font(31),fill='#ffffff')
    d.rounded_rectangle((31,567,819,579),radius=5,fill='#244659')
    d.rounded_rectangle((31,567,31+max(10,int(788*(i+1)/DURATION)),579),radius=5,fill=accent)
    return card

def extract_capture(capture, folder):
    out=Path(folder)/'screen_%04d.jpg'
    run(['ffmpeg','-hide_banner','-loglevel','error','-y','-i',capture,
         '-vf','fps=30,crop=960:350:0:0,scale=800:292',
         '-q:v','3',out])
    frames=sorted(Path(folder).glob('screen_*.jpg'))
    if len(frames)<90: raise ValueError(f'Capture too short: {len(frames)} frames')
    return frames

def render(source, capture, output, genre='sales_business', target=20, actual=12,
           fictional_data=False, synthetic_capture=False, synthetic_source=False):
    validate(genre,target,actual,fictional_data)
    source,capture,output=map(Path,(source,capture,output))
    if not source.is_file() or not capture.is_file(): raise FileNotFoundError('Missing source or capture')
    output.parent.mkdir(parents=True,exist_ok=True)
    src=probe(source)
    sv=next(x for x in src['streams'] if x['codec_type']=='video')
    sa=next(x for x in src['streams'] if x['codec_type']=='audio')
    if (sv['width'],sv['height'],sv['avg_frame_rate'])!=(W,H,'30/1'):
        raise ValueError('Expected 1080x1920 30fps source')
    if sa['codec_name']!='aac' or sa['sample_rate']!='48000':
        raise ValueError('Expected 48kHz AAC source audio')
    cap=probe(capture)
    cv=next(x for x in cap['streams'] if x['codec_type']=='video')
    if cv['width']<960 or cv['height']<350: raise ValueError('Capture smaller than crop')
    with tempfile.TemporaryDirectory(prefix='cycle813_') as td:
        td=Path(td); captured=td/'captured';captured.mkdir()
        frames=extract_capture(capture,captured)
        overlay=td/'overlays';overlay.mkdir()
        for i in range(DURATION):
            with Image.open(frames[source_index(i,len(frames))]) as f:
                draw_card(i,f,genre,target,actual,synthetic_capture).save(overlay/f'{i:03d}.png')
        fc=(f'[1:v]format=rgba,setpts=PTS-STARTPTS+{START}/{FPS}/TB[card];'
            f'[0:v][card]overlay=x={CARD_X}:y={CARD_Y}:eof_action=pass:shortest=0:'
            f'format=auto:enable=\'between(n,{START},{START+DURATION-1})\'[v]')
        run(['ffmpeg','-hide_banner','-loglevel','error','-y','-i',source,
             '-framerate',str(FPS),'-start_number','0','-i',overlay/'%03d.png',
             '-filter_complex',fc,'-map','[v]','-map','0:a:0','-c:v','libx264',
             '-preset','veryfast','-crf','21','-pix_fmt','yuv420p',
             '-frames:v',str(TOTAL),'-c:a','copy','-movflags','+faststart',output])
    p=probe(output)
    v=next(x for x in p['streams'] if x['codec_type']=='video')
    a=next(x for x in p['streams'] if x['codec_type']=='audio')
    if (v['width'],v['height'],v['avg_frame_rate'],int(v['nb_frames']))!=(W,H,'30/1',TOTAL):
        raise RuntimeError('Video QA mismatch')
    if a['codec_name']!='aac' or a['sample_rate']!='48000': raise RuntimeError('Audio QA mismatch')
    if abs(float(p['format']['duration'])-TOTAL/FPS)>0.06: raise RuntimeError('Duration mismatch')
    run(['ffmpeg','-v','error','-xerror','-i',output,'-f','null','-'])
    original_audio,new_audio=audio_sha(source),audio_sha(output)
    if original_audio!=new_audio: raise RuntimeError('Inherited AAC bitstream changed')
    qa={'cycle':813,'genre':genre,'source_cycle':812,
        'source_sha256':sha(source),'capture_sha256':sha(capture),'output_sha256':sha(output),
        'capture_type':'synthetic_ci_fixture' if synthetic_capture else 'local_real_libreoffice_calc',
        'synthetic_source':synthetic_source,'real_spreadsheet_gui_capture':not synthetic_capture,
        'fictional_data':fictional_data,'metric_target':target,'metric_actual':actual,
        'scene_replaced_frames':[START,START+DURATION-1],
        'video_width':W,'video_height':H,'fps':FPS,'frames':TOTAL,
        'duration_seconds':float(p['format']['duration']),
        'audio_codec':a['codec_name'],'audio_sample_rate':a['sample_rate'],
        'aac_bitstream_identical':True,'aac_adts_sha256':new_audio,
        'japanese_narration_inherited':not synthetic_source,
        'japanese_voice_semantics_verified':False,'japanese_caption_display_sampled':False,
        'caption_semantics_verified':False,'caption_region_outside_overlay':True,
        'full_av_decode_pass':True,'smartphone_verified':False,'asset_rights_approved':False,
        'employee_approved':False,'publication_approved':PUBLICATION_APPROVED,
        'auto_post':AUTO_POST,'private_review_only':True}
    (output.parent/'cycle813_qa.json').write_text(json.dumps(qa,ensure_ascii=False,indent=2),encoding='utf-8')
    return qa

if __name__=='__main__':
    p=argparse.ArgumentParser()
    p.add_argument('--source',required=True)
    p.add_argument('--capture',required=True)
    p.add_argument('--output',required=True)
    p.add_argument('--genre',default='sales_business',choices=tuple(GENRE_ACCENTS))
    p.add_argument('--target',type=int,default=20)
    p.add_argument('--actual',type=int,default=12)
    p.add_argument('--fictional-data',action='store_true',required=True)
    p.add_argument('--synthetic-capture',action='store_true')
    p.add_argument('--synthetic-source',action='store_true')
    a=p.parse_args()
    print(json.dumps(render(a.source,a.capture,a.output,a.genre,a.target,a.actual,
                            a.fictional_data,a.synthetic_capture,a.synthetic_source),ensure_ascii=False,indent=2))
