from pathlib import Path
import ast
p=Path(__file__).with_name("render.py")
tree=ast.parse(p.read_text(encoding="utf-8"))
assert len([n for n in ast.walk(tree) if isinstance(n,ast.FunctionDef) and n.name=="render"])==1
source=p.read_text(encoding="utf-8")
assert '"24"' in source and '"720,1280"' not in source
assert "SCENES" in source and "faststart" in source
print("3 static checks PASS; runtime video/audio verification separate")
