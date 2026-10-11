"""Japanese speech input contract for cycle488."""
SCRIPTS = (
    "メール返信、毎回ゼロから考えていませんか。",
    "相手の要望、伝える事実、返信期限を整理します。",
    "この要点から、丁寧な返信案を作って、と依頼します。",
    "AIの文章が、元の内容と合っているか確認します。",
    "名前や日付、約束した内容は必ず自分で確認。",
    "下書きを時短に使って、最終判断は自分で。",
)
GENRES = ("ai_workflow","beauty","romance","money","sales","career","health","science","travel","comparison")
def locate():
    import shutil
    from pathlib import Path
    binary = shutil.which("open_jtalk")
    voices = list(Path("/usr/share").rglob("*.htsvoice"))
    dictionaries = [p for p in Path("/var/lib/mecab/dic").glob("**/") if (p/"sys.dic").exists()]
    if not binary or not voices or not dictionaries:
        raise RuntimeError("JAPANESE_TTS_UNAVAILABLE")
    return binary, voices[0], dictionaries[0]

def synthesize(output="output/cycle488/voice"):
    import subprocess, wave, json
    from pathlib import Path
    binary, voice, dictionary = locate()
    output = Path(output)
    output.mkdir(parents=True, exist_ok=True)
    report = []
    for i, script in enumerate(SCRIPTS, 1):
        wav = output / ("voice_%02d.wav" % i)
        result = subprocess.run([binary, "-x", str(dictionary), "-m", str(voice), "-r", "1.15", "-ow", str(wav)], input=script+"\n", text=True, capture_output=True)
        if result.returncode or not wav.is_file():
            raise RuntimeError("JAPANESE_TTS_FAILED")
        with wave.open(str(wav)) as f:
            seconds = f.getnframes()/f.getframerate()
            if seconds < 0.4:
                raise RuntimeError("JAPANESE_TTS_TOO_SHORT")
        report.append({"scene": i, "seconds": round(seconds, 3)})
    (output/"voice_report.json").write_text(json.dumps(report, ensure_ascii=False, indent=2))
    return report

if __name__ == "__main__":
    print(synthesize())
