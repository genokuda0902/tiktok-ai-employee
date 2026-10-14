from pathlib import Path
import json

config = json.loads((Path(__file__).parent / 'config.json').read_text())
assert config['panel'] == [960, 700]
assert config['render_scale'] == 2
assert config['genre_count'] == 10
