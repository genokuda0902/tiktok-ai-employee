from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parent))
from render import CAPTIONS, filtergraph

def test_caption_intervals():
    graph=filtergraph()
    assert len(CAPTIONS)==4
    for start,end in [(0,3),(3,6),(6,9),(9,12)]:
        assert f"between(t,{start},{end})" in graph

def test_colon_escaped():
    assert r"SUM(B2\:B5)" in filtergraph()
