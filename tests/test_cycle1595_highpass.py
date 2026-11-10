from pathlib import Path

def test_pipeline_keeps_video_stream_and_highpass():
    text = (Path(__file__).resolve().parents[1] / "tools/cycle1595_highpass.py").read_text()
    assert '"-c:v", "copy"' in text
    assert '"highpass=f=75"' in text
    assert '"+faststart"' in text

def test_no_auto_posting():
    text = (Path(__file__).resolve().parents[1] / "tools/cycle1595_highpass.py").read_text()
    assert "upload" not in text and "publish" not in text
