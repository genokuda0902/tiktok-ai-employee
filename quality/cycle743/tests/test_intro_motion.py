from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parent))
from intro_motion import GENRES, VALUES, FPS, FRAMES, progress, render_panel

def test_genres_and_arithmetic():
    assert len(GENRES) == 10
    assert sum(VALUES) == 65
    assert FRAMES / FPS == 3.2

def test_progress_is_monotonic():
    for i in range(4):
        series = [progress(j/30, i) for j in range(FRAMES)]
        assert series == sorted(series)
        assert series[-1] > 0.999

def test_render_each_genre():
    for genre in GENRES:
        assert render_panel(2.9, genre).size == (498, 435)
