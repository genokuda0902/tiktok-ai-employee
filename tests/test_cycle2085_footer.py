from pathlib import Path
import ast
p=Path(__file__).resolve().parents[1]/"tools"/"cycle2085_footer.py"
ast.parse(p.read_text(encoding="utf-8"))
assert "公開品質は未承認" in p.read_text(encoding="utf-8")
assert "1080" in p.read_text(encoding="utf-8")
