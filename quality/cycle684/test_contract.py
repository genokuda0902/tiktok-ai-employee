from constants import WIDTH, HEIGHT, FPS, GENRES

def test_contract():
    assert (WIDTH, HEIGHT, FPS) == (1080, 1920, 30)
    assert len(GENRES) == 10
    assert len(set(GENRES)) == 10
