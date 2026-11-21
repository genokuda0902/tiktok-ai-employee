"""Cycle1624: public-safe image-first review renderer (reimplementation, not v33)."""
import json
import subprocess
from pathlib import Path

SCENES = [
    ("表記ゆれで集計ミス？", "同じ商品名なのに別々に集計される"),
    ("置換前に候補を確認", "似た名前を一覧化して誤変換を防ぐ"),
    ("統一後に再集計", "変更履歴を残し数字を再チェック"),
]

def caption_manifest():
    return [{"start": i * 4, "end": (i + 1) * 4, "text": title}
            for i, (title, _) in enumerate(SCENES)]

def validate_captions(captions, duration=12):
    assert captions and captions[0]["start"] == 0
    assert captions[-1]["end"] == duration
    assert all(a["end"] == b["start"] for a, b in zip(captions, captions[1:]))
    assert all(c["end"] > c["start"] and c["text"] for c in captions)

def validate_video(path):
    result = subprocess.run(["ffprobe", "-v", "error", "-show_entries",
        "stream=codec_type,width,height:format=duration", "-of", "json", str(path)],
        check=True, capture_output=True, text=True)
    data = json.loads(result.stdout)
    assert any(s.get("codec_type") == "video" and s.get("width") == 720
               and s.get("height") == 1280 for s in data["streams"])
    assert abs(float(data["format"]["duration"]) - 12) < .2
    subprocess.run(["ffmpeg", "-v", "error", "-i", str(path), "-f", "null", "-"],
                   check=True)
    return {"has_japanese_narration": False, "publication_approved": False}

if __name__ == "__main__":
    import sys
    validate_captions(caption_manifest())
    if len(sys.argv) > 1:
        print(json.dumps(validate_video(Path(sys.argv[1]))))
    else:
        print(json.dumps(caption_manifest(), ensure_ascii=False))
