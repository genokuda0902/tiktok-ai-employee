"""Cycle725: outcome-first 0-1.5s proof hook and pixel-checked captions.
Review-only reimplementation; all displayed numbers are synthetic.
Reuses cycle720's eight-scene Japanese Kokoro TTS, never the private v33 audio.
"""
from pathlib import Path
import json
from PIL import Image, ImageDraw
import cycle720_render as base

GENRES=base.GENRES
SALES=base.SALES
HOOK="4か月の売上、合計65万円"
HOOK_VOICE="四か月の売上、合計六十五万円。AIで見える化します。"
SAFE_LEFT=41
SAFE_RIGHT=460
CAPTION_FONT=22
ORIGINAL_CARD=base.card

def wrap_pixels(text, font, max_width=SAFE_RIGHT-SAFE_LEFT):
    """Wrap by rendered Japanese glyph width, not by code-point count."""
    if not text:
        raise ValueError("empty caption")
    lines=[]
    line=""
    for char in text:
        trial=line+char
        if font.getlength(trial)>max_width and line:
            lines.append(line)
            line=char
        else:
            line=trial
    if line:
        lines.append(line)
    if len(lines)>2:
        raise ValueError("caption exceeds two-line safe area: "+text)
    if any(font.getlength(line)>max_width for line in lines):
        raise ValueError("caption width overflow: "+text)
    return lines

def proof_card(path):
    im=Image.open(path).convert("RGB")
    d=ImageDraw.Draw(im)
    d.rounded_rectangle((38,265,502,702),radius=26,fill="#0b314c",outline="#6ff2e4",width=4)
    d.rounded_rectangle((66,294,474,355),radius=15,fill="#184b67")
    base.write(d,85,308,"RESULT FIRST / 架空データ",19,"#b4fff4")
    base.write(d,75,385,"4か月の売上を",29,"#ffffff")
    base.write(d,71,457,"65万円",77,"#79fff0")
    base.write(d,80,570,"AIでグラフにする",26,"#ffffff")
    base.write(d,80,636,"※ 最後は人が検算",20,"#ffdfa1")
    im.save(path)

def safe_caption(path, text):
    im=Image.open(path).convert("RGB")
    d=ImageDraw.Draw(im)
    d.rounded_rectangle((25,752,476,865),radius=17,fill="#153349")
    font=base.font(CAPTION_FONT)
    lines=wrap_pixels(text,font)
    for n,line in enumerate(lines):
        d.text((SAFE_LEFT,773+n*40),line,font=font,fill="#ffffff")
    im.save(path)
    return lines

def card(i,path):
    ORIGINAL_CARD(i,path)
    if i==0:
        proof_card(path)
    safe_caption(path,base.SCENES[i][1])

def validate_contract():
    assert len(GENRES)==10 and len(set(GENRES))==10
    assert sum(SALES)==65
    assert "65" in HOOK and "六十五" in HOOK_VOICE
    assert base.SCENES[0][1]==HOOK_VOICE
    for heading,voice,kind in base.SCENES:
        wrap_pixels(voice,base.font(CAPTION_FONT))
    return True

def main():
    base.OUT=Path("output/cycle725")
    base.SCENES[0]=(HOOK,HOOK_VOICE,"before")
    base.card=card
    validate_contract()
    base.main()
    out=base.OUT
    src=out/"cycle720_NARRATED_REVIEW_ONLY.mp4"
    dst=out/"cycle725_OUTCOME_FIRST_NARRATED_REVIEW_ONLY.mp4"
    src.rename(dst)
    report=json.loads((out/"report.json").read_text(encoding="utf-8"))
    report.update({
        "cycle":725,"video":str(dst),
        "change":"0s outcome-first 65-man-yen proof hook + pixel-measured caption wrapping",
        "first_narration":HOOK_VOICE,
        "safe_caption_bounds":[SAFE_LEFT,752,SAFE_RIGHT,865],
        "genres_configured":list(GENRES),
        "genres_render_verified":["ai_work"],
        "reference_v33":"not embedded, not redistributed",
        "review_only":True,"publication_approved":False,
        "human_pronunciation_review":False,
        "subtitle_sync":"scene-level measured TTS duration, word-level not verified",
    })
    (out/"report.json").write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding="utf-8")
    print("CYCLE725_MP4",dst)
if __name__=="__main__":
    main()
