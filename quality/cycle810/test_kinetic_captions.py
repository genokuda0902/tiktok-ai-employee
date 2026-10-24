"""Zero-dependency contract tests for cycle810."""
import importlib.util
from pathlib import Path

p = Path(__file__).with_name("kinetic_captions.py")
spec = importlib.util.spec_from_file_location("engine", p)
engine = importlib.util.module_from_spec(spec)
spec.loader.exec_module(engine)

def test_ten_genres():
    assert len(set(engine.GENRES)) == 10
    assert set(engine.GENRES) == set(engine.PALETTE)

def test_japanese_text_and_eight_scenes():
    assert len(engine.CHUNKS) == 8
    assert all(len(chunks) == 3 for chunks in engine.CHUNKS)
    assert all(any("\u3040" <= c <= "\u9fff" for c in "".join(chunks)) for chunks in engine.CHUNKS)

def test_frame_conservation():
    for frames in range(9, 150):
        for chunks in engine.CHUNKS:
            result = engine.allocate_frames(frames, chunks)
            assert sum(result) == frames
            assert min(result) >= 3

def test_timeline_24_phases():
    timeline = engine.build_timeline([101, 93, 91, 99, 98, 101, 89, 103])
    assert len(timeline) == 24
    assert timeline[0]["start_frame"] == 0
    assert timeline[-1]["start_frame"] + timeline[-1]["frames"] == 775
    assert all(row["full_subtitle"] == "".join(engine.CHUNKS[row["scene"] - 1]) for row in timeline)

def test_reject_invalid():
    try:
        engine.allocate_frames(8, ["a", "b", "c"])
    except ValueError:
        pass
    else:
        raise AssertionError("Too-short scene was accepted")

def test_publication_blocked():
    assert not engine.AUTO_POST
    assert not engine.EMPLOYEE_APPROVAL
    engine.validate_review_gate("sales_business")
    for genre in ("unsupported",):
        try:
            engine.validate_review_gate(genre)
        except ValueError:
            pass
        else:
            raise AssertionError("Unknown genre accepted")
    try:
        engine.validate_review_gate("sales_business", approved=True)
    except PermissionError:
        pass
    else:
        raise AssertionError("Approval gate bypassed")

if __name__ == "__main__":
    for name, value in list(globals().items()):
        if name.startswith("test_") and callable(value):
            value()
    print("6 contract tests PASS")
