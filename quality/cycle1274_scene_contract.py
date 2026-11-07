"""Review-only four-scene contract; no publication approval implied."""
SCENES = [
    ("AIの答え、そのまま使う？", 2.0),
    ("確認せずに提出", 2.0),
    ("出典・日付・数字", 2.0),
    ("最後は人が判断", 2.0),
]
def validate_scenes(scenes):
    if len(scenes) != 4 or any(not text or seconds <= 0 for text, seconds in scenes):
        raise ValueError("Invalid scene contract")
    if abs(sum(seconds for _, seconds in scenes) - 8.0) > 0.001:
        raise ValueError("Duration must be 8 seconds")
    return True

def test_contract():
    assert validate_scenes(SCENES)
    try:
        validate_scenes([("missing", 2.0)])
    except ValueError:
        pass
    else:
        raise AssertionError("invalid input accepted")

if __name__ == "__main__":
    test_contract()
