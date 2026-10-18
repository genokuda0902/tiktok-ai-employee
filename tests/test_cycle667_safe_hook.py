import json
from pathlib import Path
p=Path('quality/cycle667/contract.json')
d=json.loads(p.read_text())
assert len(d['genres'])==10
assert sum(d['numbers'])==d['expected_sum']
assert d['publication']=='NOT_APPROVED'
