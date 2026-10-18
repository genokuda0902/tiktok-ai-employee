"""Review-only Open JTalk Japanese TTS probe; no external service."""
import json
import shutil
import subprocess
from pathlib import Path

def synthesize(text, output):
    if not text or len(text) > 120 or "\n" in text:
        raise ValueError("Invalid sentence")
    binary = shutil.which("open_jtalk")
    dictionary = Path("/var/lib/mecab/dic/open-jtalk/naist-jdic")
    voices = list(Path("/usr/share").rglob("*.htsvoice"))
    if not binary or not dictionary.is_dir() or not voices:
        raise FileNotFoundError("Offline Japanese TTS dependencies missing")
    output = Path(output)
    output.parent.mkdir(parents=True, exist_ok=True)
    subprocess.run([binary, "-x", str(dictionary), "-m", str(voices[0]),
                    "-ow", str(output)], input=text, text=True, check=True)
    if output.stat().st_size < 2000:
        raise RuntimeError("No actual voice output")
    return str(output)

if __name__ == "__main__":
    import argparse
    p = argparse.ArgumentParser()
    p.add_argument("--output", required=True)
    args = p.parse_args()
    print(json.dumps({"wav": synthesize("合計は六百五十です。", args.output),
                      "publication": "NOT_APPROVED"}, ensure_ascii=False))
