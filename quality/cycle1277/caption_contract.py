"""Review-only caption timing contract, not a publication gate."""
SCENES = [("AIの回答、そのまま使う？", 3), ("根拠がないまま提出", 3), ("出典・日付・数字を照合", 3), ("最後は人が判断", 3)]

def srt(scenes=SCENES):
    result = []
    elapsed = 0
    for i, (caption, seconds) in enumerate(scenes, 1):
        assert caption and seconds > 0
        start, end = elapsed, elapsed + seconds
        def timestamp(t): return f"00:00:{t:02d},000"
        result.append(f"{i}\n{timestamp(start)} --> {timestamp(end)}\n{caption}\n")
        elapsed = end
    return "\n".join(result)

def test_caption_coverage():
    assert sum(seconds for _, seconds in SCENES) == 12
    assert "00:00:09,000 --> 00:00:12,000" in srt()
    assert len(srt().split("-->")) == 4

if __name__ == "__main__":
    test_caption_coverage()
    print(srt())
