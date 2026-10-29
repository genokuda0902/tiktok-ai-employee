"""cycle966: LibreOffice Calc-recalculated fictional table -> 3 visual proof beats.
Only locally authorized MP4s; never publish, merge, or post automatically.
"""
import argparse, csv, hashlib, json, re, subprocess
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

ROWS = [('4月',12,8),('5月',16,9),('6月',18,12)]
GENRE_COLORS = {'ai_work':'#35d4c5','business':'#76baff','finance':'#e5bb69','education':'#f3ac75','career':'#9bb8ff','wellness':'#87d4a1','lifestyle':'#e7a6cd','technology':'#5ac5e8','travel':'#e2b98e','trivia':'#c7a5f0'}
REVIEWED_GENRES = {'ai_work'}
START,END = 174,261  # frame [174,261): 5.80-8.70s, 87 frames
FONT='/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc'
BOLD='/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc'

def run(cmd,timeout=240):
    p=subprocess.run(list(map(str,cmd)),stdout=subprocess.PIPE,stderr=subprocess.PIPE,timeout=timeout)
    if p.returncode: raise RuntimeError((p.stderr or p.stdout).decode(errors='replace')[-3000:])
    return p.stdout.decode(errors='replace')

def sha(path):
    h=hashlib.sha256()
    with open(path,'rb') as f:
        for block in iter(lambda:f.read(1<<20),b''):h.update(block)
    return h.hexdigest()

def build_calc_export(out):
    out=Path(out);out.mkdir(parents=True,exist_ok=True)
    csvpath=out/'fictional_sales.csv'
    with csvpath.open('w',encoding='utf-8-sig',newline='') as f:
        w=csv.writer(f);w.writerow(['月','営業A','営業B']);w.writerows(ROWS)
        w.writerow(['合計','=SUM(B2:B4)','=SUM(C2:C4)'])
    # LibreOffice actually calculates SUM formulas on CSV import; this is not a screen recording.
    profile=(out/'lo-profile').resolve().as_uri()
    run(['libreoffice',f'-env:UserInstallation={profile}','--headless','--convert-to','pdf','--outdir',out,csvpath],90)
    pdf=out/'fictional_sales.pdf'
    text=run(['pdftotext','-layout',pdf,'-'],30)
    if not re.search(r'合計\s+46\s+29',text):
        raise ValueError('LibreOffice did not independently calculate expected 46 and 29: '+text[-500:])
    run(['pdftoppm','-f','1','-l','1','-r','240','-png','-singlefile',pdf,out/'calc_page'],60)
    return csvpath,pdf,out/'calc_page.png',text

def font(sz,bold=False):return ImageFont.truetype(BOLD if bold else FONT,sz)

def make_stages(page_path,out):
    out=Path(out);out.mkdir(parents=True,exist_ok=True)
    raw=Image.open(page_path).convert('RGB')
    # Crop actual Calc PDF around the cells, never redraw fake UI.
    crop=raw.crop((130,220,750,560))
    outputs=[]
    for step in range(3):
        im=Image.new('RGB',(1080,1450),'#061a2d');d=ImageDraw.Draw(im)
        d.rounded_rectangle((42,28,1038,1400),radius=38,outline='#2c7998',width=3,fill='#08243a')
        d.text((76,65),'AI仕事術 / REAL CALC OUTPUT',font=font(29,True),fill='#83dce9')
        d.text((74,147),'完成形を、実データ計算で確認',font=font(49,True),fill='white')
        d.text((75,220),'架空データをLibreOffice Calcで再計算・PDF出力',font=font(24),fill='#b9d2de')
        d.rounded_rectangle((64,296,1016,825),radius=25,fill='#eaf2f6')
        if step==0:
            d.text((95,318),'STEP 1  表計算の完成見本',font=font(35,True),fill='#173b52')
        elif step==1:
            d.text((95,318),'STEP 2  月別データを可視化',font=font(35,True),fill='#173b52')
        else:
            d.text((95,318),'STEP 3  合計値を元データと照合',font=font(35,True),fill='#173b52')
        table=crop.resize((750,415),Image.Resampling.LANCZOS)
        im.paste(table,(164,388))
        d=ImageDraw.Draw(im)
        d.rounded_rectangle((64,865,1016,1255),radius=24,fill='#10364b',outline='#287e98',width=2)
        if step==0:
            d.text((104,901),'3か月の架空売上データ',font=font(36,True),fill='#ffffff')
            d.text((104,986),'4月 → 5月 → 6月',font=font(47,True),fill='#78e5df')
            d.text((104,1100),'完成例を先に見せて、作業を明確にする',font=font(27),fill='#c3dbe3')
        elif step==1:
            d.text((104,900),'月別の比較',font=font(34,True),fill='#ffffff')
            for j,(label,a,b) in enumerate(ROWS):
                y=973+j*75;d.text((105,y),label,font=font(30,True),fill='#d4e9f2')
                d.rounded_rectangle((230,y+4,230+a*23,y+32),radius=8,fill='#35d4c5')
                d.rounded_rectangle((230,y+39,230+b*23,y+65),radius=8,fill='#7baaff')
            d.text((770,1050),'A / B',font=font(25,True),fill='#d4e9f2')
        else:
            d.text((104,902),'LibreOfficeが計算した合計',font=font(32,True),fill='white')
            d.text((104,974),'営業A',font=font(30),fill='#c5e3ec');d.text((305,954),'46',font=font(91,True),fill='#45e0ce')
            d.text((590,974),'営業B',font=font(30),fill='#c5e3ec');d.text((796,954),'29',font=font(91,True),fill='#a8c4ff')
            d.text((104,1125),'SUM関数の実計算結果と一致',font=font(27),fill='#d8e9ee')
        d.text((80,1322),'※画面はPDF出力を編集した説明映像。操作録画ではありません。',font=font(22),fill='#b6c9d5')
        path=out/f'stage_{step+1}.png';im.save(path);outputs.append(path)
    return outputs

def render(source,stages,output):
    # Keep lower burned captions (y>=1450), copy AAC bitstream.
    filters="[0:v][1:v]overlay=0:0:enable='between(n,174,202)'[v1];[v1][2:v]overlay=0:0:enable='between(n,203,231)'[v2];[v2][3:v]overlay=0:0:enable='between(n,232,260)'[v3]"
    cmd=['ffmpeg','-hide_banner','-loglevel','error','-y','-i',source]
    for s in stages:cmd+=['-loop','1','-framerate','30','-i',s]
    cmd+=['-filter_complex',filters,'-map','[v3]','-map','0:a:0','-c:v','libx264','-preset','veryfast','-crf','19','-pix_fmt','yuv420p','-c:a','copy','-frames:v','691','-metadata:s:a:0','language=jpn','-movflags','+faststart',output]
    run(cmd,480)

def main():
    p=argparse.ArgumentParser();p.add_argument('--source');p.add_argument('--output');p.add_argument('--workdir',required=True);p.add_argument('--report');p.add_argument('--genre',default='ai_work');a=p.parse_args()
    if a.genre not in GENRE_COLORS:raise ValueError('Unknown genre')
    if a.genre not in REVIEWED_GENRES:raise PermissionError('Unreviewed genre is blocked')
    if bool(a.source)!=bool(a.output):raise ValueError('Source and output must be supplied together')
    wd=Path(a.workdir);csvpath,pdf,png,text=build_calc_export(wd)
    stages=make_stages(png,wd)
    result={'cycle':966,'genre':a.genre,'source_kind':'fictional_csv_recalculated_by_LibreOffice_Calc','calc_verified_totals':[46,29], 'scene_frames':[START,END], 'source':str(a.source or ''),'output':str(a.output or ''),'publication_approved':False,'employee_review_required':True,'asr_semantic_verified':False,'stage_pngs':[str(x) for x in stages]}
    if a.source:
        result['input_sha256']=sha(a.source);render(a.source,stages,a.output);result['output_sha256']=sha(a.output)
    if a.report:Path(a.report).write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
    print(json.dumps(result,ensure_ascii=False))
if __name__=='__main__':main()
