from render_scene3 import frame, full_frame, COLORS, FPS, N
from PIL import ImageChops

def test_renderer():
    assert (FPS, N) == (30, 60)
    assert frame(0).size == (736, 604)
    assert full_frame(59).size == (870, 792)
    assert len(COLORS) == 10
    for genre in COLORS:
        assert full_frame(20, genre).size == (870, 792)
    assert ImageChops.difference(frame(0), frame(55)).getbbox() is not None

if __name__ == '__main__':
    test_renderer()
    print('PASS: scene3 storyboard contract')
