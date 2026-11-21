import ast
from pathlib import Path
p=Path(__file__).with_name("render.py")
source=p.read_text()
tree=ast.parse(source)
assert "posting_allowed" in source and "False" in source
assert "SCENES" in source and "ffmpeg" in source
assert "employee_approved" in source
assert "IMG_5805" not in source
print("4 static checks PASS; rendering and audio remain separately unverified")
