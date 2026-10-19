from hook_contract import PALETTES, WIDTH, HEIGHT, FPS, HOOK_SECONDS, validate_hook

def test_contract():
    assert len(PALETTES) == 10
    assert (WIDTH, HEIGHT, FPS, HOOK_SECONDS) == (1080, 1920, 30, 2.1)
    for genre in PALETTES:
        assert validate_hook(genre, "ただの基板？", "パソコンです。", (0, 0, 1080, 1360))

if __name__ == "__main__":
    test_contract()
    print("PASS: 10 genres, 1080x1920, caption-safe first-second hook")
