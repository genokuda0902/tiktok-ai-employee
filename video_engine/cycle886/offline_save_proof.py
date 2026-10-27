"""Cycle886: local Chromium proof of input -> arithmetic check -> save (REVIEW ONLY).

This is a reimplementation, not original v33. Browser UI is original HTML,
with fictional data; no real ChatGPT/Excel API, network, or personal data.
Completed inherited-audio MP4 must remain outside GitHub.
"""
from __future__ import annotations
import argparse,hashlib,json,re,subprocess
from pathlib import Path
from dataclasses import dataclass

GENRES=("ai_productivity","beauty","romance_psychology","money_saving","sales_business","career","health_lifestyle","trivia_science","travel_food","product_lifestyle")
FPS=30; START=510; END=588; FRAMES=691; CAPTION_TOP=1438
POLICY={"review_only":True,"publication_approved":False,"external_upload":False,"automatic_posting":False,"source_rights_reviewed":False,"offline_fictional_data":True}
FONT="/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc"

@dataclass(frozen=True)
class Story:
    genre:str
    headline:str
    purpose:str
    save_label:str

STORIES={
"ai_productivity":Story("ai_productivity","指示を保存して、次回は一瞬","売上集計","テンプレート保存"),
"beauty":Story("beauty","手順を残して、次回も迷わない","美容メモ","手順を保存"),
"romance_psychology":Story("romance_psychology","気づきを記録して振り返る","会話メモ","メモを保存"),
"money_saving":Story("money_saving","家計の確認を習慣にする","家計集計","集計を保存"),
"sales_business":Story("sales_business","検算した手順を残す","営業集計","手順を保存"),
"career":Story("career","作業の型を保存する","業務手順","手順を保存"),
"health_lifestyle":Story("health_lifestyle","日々の記録を残す","生活記録","記録を保存"),
"trivia_science":Story("trivia_science","根拠を確認して保存","検証メモ","メモを保存"),
"travel_food":Story("travel_food","計画を残して使い回す","旅行計画","計画を保存"),
"product_lifestyle":Story("product_lifestyle","比較条件を残しておく","商品比較","比較を保存")}

def sha256(path):
    h=hashlib.sha256()
    with open(path,"rb") as f:
        for chunk in iter(lambda:f.read(1024*1024),b""):h.update(chunk)
    return h.hexdigest()

def validate_story(s):
    if s.genre not in GENRES:raise ValueError("unknown genre")
    for text in (s.headline,s.purpose,s.save_label):
        if not text or len(text)>26 or re.search(r"https?://|@|[\r\n<>]|\d{3}[- ]?\d{4}",text):
            raise ValueError("unsafe copy")
    return True

def validate_manifest(m,source):
    if any(m.get(k)!=v for k,v in POLICY.items()):raise ValueError("unapproved media policy")
    if m.get("source_sha256")!=sha256(source):raise ValueError("source hash mismatch")
    return True

def stage(f):
    if not 0<=f<END-START:raise ValueError("frame outside scene")
    return 0 if f<26 else 1 if f<52 else 2

def html_document():
    return """<!doctype html><html lang="ja"><meta charset="utf-8"><style>
    *{box-sizing:border-box}body{margin:0;background:#e9f1f5;color:#102b43;font-family:Arial,sans-serif}
    header{background:#133c58;color:white;padding:16px 22px;font-size:20px;font-weight:bold}
    main{padding:16px 24px}.tag{font-size:14px;color:#286078;margin-bottom:10px}
    .cols{display:grid;grid-template-columns:1fr 1fr;gap:16px}
    .panel{background:white;border:2px solid #b4d3df;border-radius:12px;padding:14px;min-height:235px}
    h2{margin:0 0 8px;font-size:21px}.tiny{font-size:14px;color:#446176;margin-bottom:10px}
    textarea{width:100%;height:100px;border:2px solid #7aa9bf;border-radius:9px;padding:12px;font-size:18px}
    button{border:0;border-radius:9px;background:#007f9d;color:white;font-size:17px;font-weight:bold;padding:12px 20px;margin-top:8px}
    button:disabled{background:#9aadb5}#save{background:#1567b6;margin-left:8px}
    #status{font-size:19px;font-weight:bold;color:#117a52}.data{font-size:17px;line-height:1.8}
    .result{background:#d9f6f0;padding:12px;border-radius:8px;font-size:19px;font-weight:bold}
    </style><header>LOCAL WORKFLOW DEMO ｜ 架空データ</header><main>
    <div class="tag">実在サービスの画面ではありません／ネット接続なし</div>
    <div class="cols"><div class="panel"><h2>① 指示を作る</h2><div class="tiny">入力内容は端末内だけで処理</div>
    <textarea id="prompt"></textarea><button id="verify" onclick="verify()">集計を検証</button>
    <button id="save" onclick="save()" disabled>テンプレート保存</button></div>
    <div class="panel"><h2>② 元データと照合</h2><div class="data">営業A：12 / 16 / 18<br>営業B：8 / 9 / 12</div>
    <div id="result" class="result">検算待ち</div><p id="status">未保存</p></div></div></main>
    <script>const data={A:[12,16,18],B:[8,9,12]};let verified=false;
    function verify(){let a=data.A.reduce((x,y)=>x+y,0),b=data.B.reduce((x,y)=>x+y,0);
    document.getElementById('result').textContent=`検算OK｜営業A ${a} / 営業B ${b}`;
    document.getElementById('save').disabled=false;verified=true;}
    function save(){if(!verified)return;const p=document.getElementById('prompt').value;
    if(!p.trim())return;window.savedTemplate={prompt:p,checked:true};
    document.getElementById('status').textContent='保存済み ✓';}</script></html>"""

def capture_browser(out):
    from playwright.sync_api import sync_playwright
    out=Path(out);out.mkdir(parents=True,exist_ok=True)
    with sync_playwright() as p:
        browser=p.chromium.launch(headless=True,executable_path="/usr/bin/chromium",args=["--no-sandbox","--disable-gpu"])
        page=browser.new_page(viewport={"width":1000,"height":480},device_scale_factor=1)
        page.route("**/*",lambda route:route.abort())
        page.set_content(html_document(),wait_until="load")
        page.locator("#prompt").fill("架空の売上データを集計し、元の数値と照合する。")
        page.screenshot(path=str(out/"01_input.png"))
        page.locator("#verify").click()
        assert page.locator("#result").inner_text()=="検算OK｜営業A 46 / 営業B 29"
        page.screenshot(path=str(out/"02_verified.png"))
        page.locator("#save").click()
        assert page.locator("#status").inner_text()=="保存済み ✓"
        assert page.evaluate("window.savedTemplate.checked") is True
        page.screenshot(path=str(out/"03_saved.png"))
        browser.close()
    hashes=[sha256(out/name) for name in ("01_input.png","02_verified.png","03_saved.png")]
    if len(set(hashes))!=3:raise RuntimeError("not three distinct browser states")
    return hashes

def draw_frame(f,screens,story=STORIES["ai_productivity"]):
    from PIL import Image,ImageDraw,ImageFont
    validate_story(story)
    i=stage(f)
    img=Image.new("RGBA",(1080,CAPTION_TOP),(0,0,0,0));d=ImageDraw.Draw(img,"RGBA")
    font=lambda n:ImageFont.truetype(FONT,n,index=0)
    d.rounded_rectangle((38,182,1042,1330),radius=35,fill=(4,21,39,246),outline=(56,188,208,230),width=3)
    d.text((75,223),story.headline,font=font(50),fill=(255,255,255,255))
    d.text((75,315),"実際のローカルブラウザー操作を記録",font=font(30),fill=(135,228,240,255))
    d.rounded_rectangle((75,375,470,431),radius=18,fill=(11,95,117,255))
    d.text((100,383),"OFFLINE DEMO / 架空",font=font(26),fill=(245,252,255,255))
    img.paste(screens[i].convert("RGB").resize((944,453),Image.Resampling.LANCZOS),(68,505))
    d.rounded_rectangle((66,503,1014,960),radius=9,outline=(121,215,233,255),width=4)
    for j,lab in enumerate(("入力","検算","保存")):
        x=95+j*322
        d.rounded_rectangle((x,1010,x+288,1114),radius=19,fill=(14,120,149,255) if j==i else (17,43,65,255),outline=(61,191,210,255),width=2)
        d.text((x+24,1033),f"{j+1}  {lab}",font=font(37),fill=(255,255,255,255))
    d.text((94,1190),("指示を入力","元データで検算","保存完了 ✓")[i],font=font(46),fill=(247,203,112,255) if i==2 else (238,249,255,255))
    return img

def overlays(out,screens):
    from PIL import Image
    out=Path(out);out.mkdir(parents=True,exist_ok=True)
    imgs=[Image.open(x).convert("RGB") for x in screens]
    for f in range(END-START):draw_frame(f,imgs).save(out/f"{f:03d}.png",compress_level=1)

def render(source,output,manifest,work):
    source=Path(source);output=Path(output);work=Path(work)
    validate_manifest(json.loads(Path(manifest).read_text()),source)
    meta=json.loads(subprocess.check_output(["ffprobe","-v","error","-show_entries","stream=codec_type,codec_name,width,height,r_frame_rate,nb_frames,sample_rate,channels","-of","json",str(source)]))
    v=next(x for x in meta["streams"] if x["codec_type"]=="video")
    a=next(x for x in meta["streams"] if x["codec_type"]=="audio")
    if (v["codec_name"],v["width"],v["height"],v["r_frame_rate"],int(v["nb_frames"]))!=("h264",1080,1920,"30/1",691):raise ValueError("source video invalid")
    if (a["codec_name"],int(a["sample_rate"]),a["channels"])!=("aac",48000,2):raise ValueError("source audio invalid")
    capture_browser(work/"browser")
    overlays(work/"overlays",[work/"browser"/x for x in ("01_input.png","02_verified.png","03_saved.png")])
    output.parent.mkdir(parents=True,exist_ok=True)
    graph=f"[1:v]setpts=PTS+{START}/({FPS}*TB)[ov];[0:v][ov]overlay=0:0:shortest=0:repeatlast=0:eof_action=pass:format=auto:enable='between(n,{START},{END-1})'[v]"
    subprocess.run(["ffmpeg","-v","error","-y","-i",str(source),"-framerate","30","-start_number","0","-i",str(work/"overlays"/"%03d.png"),"-filter_complex",graph,"-map","[v]","-map","0:a:0","-frames:v","691","-c:v","libx264","-preset","veryfast","-crf","19","-pix_fmt","yuv420p","-c:a","copy","-movflags","+faststart",str(output)],check=True,timeout=300)
    subprocess.run(["ffmpeg","-v","error","-xerror","-i",str(output),"-f","null","-"],check=True,timeout=120)
    return sha256(output)

if __name__=="__main__":
    p=argparse.ArgumentParser()
    for name in ("source","output","manifest","work-dir"):p.add_argument("--"+name,required=True)
    a=p.parse_args()
    print(json.dumps({"review_only":True,"output_sha256":render(a.source,a.output,a.manifest,a.work_dir)}))
