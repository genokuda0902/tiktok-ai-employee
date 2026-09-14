#!/usr/bin/env python3
import json
import os
import time
import urllib.parse
import urllib.request
from pathlib import Path

BASE = os.environ.get("AIVIS_URL", "http://127.0.0.1:10101")
OUT = Path(os.environ.get("NARRATION_OUT", "output/narration.wav"))
OUT.parent.mkdir(parents=True, exist_ok=True)

DEFAULT_TEXT = "そのExcelコピペ、まだ手作業ですか？長文の情報整理は、AIに必要な項目と出力形式を指定するだけで、一気にラクになります。まず元の文章を貼り付けて、氏名、電話番号、メールアドレス、希望日時を表形式で出して、と指示します。すると、バラバラだった情報が表に整理されます。あとは内容を確認して、Excelやスプレッドシートに貼り付けるだけ。毎日の面倒なコピペ作業を減らしたい人は、保存して試してみてください。"
TEXT = os.environ.get("NARRATION_TEXT", DEFAULT_TEXT)


def req(path, method="GET", data=None, content_type=None, timeout=120):
    headers = {}
    if content_type:
        headers["Content-Type"] = content_type
    r = urllib.request.Request(BASE + path, data=data, headers=headers, method=method)
    with urllib.request.urlopen(r, timeout=timeout) as res:
        return res.read()


def wait_engine():
    last = None
    for _ in range(60):
        try:
            return json.loads(req("/speakers", timeout=5).decode("utf-8"))
        except Exception as e:
            last = e
            time.sleep(2)
    raise RuntimeError(f"AivisSpeech Engine not ready: {last}")


def choose_style(speakers):
    wanted = os.environ.get("AIVIS_STYLE_ID")
    if wanted:
        return int(wanted)
    # Prefer the installed 中2 speaker. Fall back to the first available style.
    for sp in speakers:
        name = str(sp.get("name", ""))
        if "中2" in name:
            styles = sp.get("styles") or []
            if styles:
                return int(styles[0]["id"])
    for sp in speakers:
        styles = sp.get("styles") or []
        if styles:
            return int(styles[0]["id"])
    # Known global style id from the successful CI engine discovery.
    return 604166016


speakers = wait_engine()
style_id = choose_style(speakers)
print(f"Using AivisSpeech style_id={style_id}")

params = urllib.parse.urlencode({"text": TEXT, "speaker": style_id})
query = json.loads(req("/audio_query?" + params, method="POST").decode("utf-8"))
# TikTok-oriented: slightly brisk but still natural. Let the model handle pitch/prosody.
query["speedScale"] = float(os.environ.get("AIVIS_SPEED", "1.12"))
query["volumeScale"] = float(os.environ.get("AIVIS_VOLUME", "1.0"))
body = json.dumps(query, ensure_ascii=False).encode("utf-8")
wave = req("/synthesis?" + urllib.parse.urlencode({"speaker": style_id}), method="POST", data=body, content_type="application/json", timeout=300)
OUT.write_bytes(wave)
if OUT.stat().st_size < 1000:
    raise RuntimeError("Generated narration WAV is unexpectedly small")
print(f"Generated {OUT} ({OUT.stat().st_size} bytes)")
