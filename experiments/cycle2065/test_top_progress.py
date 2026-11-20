from top_progress import render
def test_render_exists():
    assert callable(render)
def test_missing_source(tmp_path):
    try:
        render(tmp_path/"missing.mp4",tmp_path/"out.mp4")
    except AssertionError:
        return
    raise AssertionError("missing source accepted")
