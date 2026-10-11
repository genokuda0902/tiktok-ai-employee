"""Generate Japanese speech using a free installed Open JTalk voice.
Fail closed when the voice or dictionary is missing; never substitute SFX for speech.
"""
from pathlib import Path
import subprocess

SCRIPTS = [
    "会議のメモ、読んだだけで終わっていませんか。",
    "まずは、決定事項、担当者、期限に分けます。",
    "決定事項、担当、期限の三つに整理して、と指示します。",
    "すると、次に何をするかが見える形になります。",
    "ただし、名前と期限は、必ず人が確認します。",
    "AIは整理役。最終確認は、自分でしましょう。",
]

def synthesize(output_dir):
    import shutil
    if not shutil.which("open_jtalk"):
        raise RuntimeError("Open JTalk unavailable")
    voices = list(Path("/usr/share").rglob("*.htsvoice"))
    dictionaries = [p for p in Path("/var/lib/mecab/dic").glob("**/") if (p/"sys.dic").exists()]
    if not voices or not dictionaries:
        raise RuntimeError("Japanese voice model or dictionary unavailable")
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    result = []
    for i, sentence in enumerate(SCRIPTS, 1):
        wav = output_dir / f"narration_{i:02d}.wav"
        subprocess.run(["open_jtalk", "-x", str(dictionaries[0]), "-m", str(voices[0]),
                        "-r", "1.2", "-ow", str(wav)], input=sentence+"\n",
                       text=True, check=True)
        if not wav.is_file() or wav.stat().st_size < 1024:
            raise RuntimeError("TTS failed or empty output")
        result.append(wav)
    return result
