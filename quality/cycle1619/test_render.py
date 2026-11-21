from pathlib import Path
import ast
p=Path(__file__).with_name("render.py")
tree=ast.parse(p.read_text(encoding="utf-8"))
assert len([n for n in ast.walk(tree) if isinstance(n,ast.FunctionDef) and n.name=="render"])==1
text=p.read_text(encoding="utf-8")
assert "REVIEW ONLY" in text
assert "720,1280" in text
assert "ffmpeg" in text
assert "商品Ａ" in text and "商品A" in text
print("cycle1619 static checks PASS; narration and synchronized captions NOT verified")
