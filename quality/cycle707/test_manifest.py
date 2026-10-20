import json
from pathlib import Path
p = Path(__file__).with_name('manifest.json')
a = json.loads(p.read_text())
assert (a['width'], a['height'], a['fps']) == (1080, 1920, 30)
assert a['genre_count'] == 10
assert a['status'] == 'HUMAN_REVIEW'
print('cycle707 manifest checks passed')
