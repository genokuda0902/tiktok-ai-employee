import ast
from pathlib import Path
p=Path(__file__).parent/'render.py'
s=p.read_text(encoding='utf-8')
ast.parse(s)
assert 'SCENES=' in s and 'REVIEW ONLY' in s
assert 'libx264' in s and 'captions.srt' in s
assert 'auto_post' not in s
print('cycle1312 static checks PASS; narration and approval NOT verified')
