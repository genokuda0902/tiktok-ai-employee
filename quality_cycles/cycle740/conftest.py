import json
from pathlib import Path
import pytest

@pytest.fixture
def genres():
    return json.loads((Path(__file__).parent / 'genres.json').read_text(encoding='utf-8'))
