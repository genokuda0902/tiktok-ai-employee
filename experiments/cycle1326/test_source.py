from pathlib import Path
import ast
p=Path(__file__).with_name("render.py")
tree=ast.parse(p.read_text(encoding="utf-8"))
assert any(isinstance(n,ast.FunctionDef) and n.name=="render" for n in ast.walk(tree))
assert "1080,1920" in p.read_text(encoding="utf-8")
assert "レビュー専用・未承認" in p.read_text(encoding="utf-8")
print("3 source checks passed")
