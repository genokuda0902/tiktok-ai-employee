from pathlib import Path
import ast
source = Path(__file__).with_name("native_ja_tts.py").read_text(encoding="utf-8")
assert "open_jtalk" in source
assert "LINES" in source
assert "voice_manifest.txt" in source
ast.parse(source)
print("cycle481 native Japanese TTS source checks PASS")
