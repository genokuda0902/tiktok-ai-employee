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
