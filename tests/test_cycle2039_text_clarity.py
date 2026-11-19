"""Integration test: requires a local sample video via CYCLE2039_SAMPLE."""
import json
import os
import subprocess
from pathlib import Path
from tools.cycle2039_text_clarity import enhance

def test_video_contract(tmp_path):
    source = os.environ.get("CYCLE2039_SAMPLE")
    if not source:
        import pytest
        pytest.skip("Set CYCLE2039_SAMPLE to a licensed input MP4")
    output = tmp_path / "enhanced.mp4"
    enhance(Path(source), output)
    info = json.loads(subprocess.check_output(["ffprobe", "-v", "error",
        "-show_streams", "-of", "json", str(output)]))
    video = next(x for x in info["streams"] if x["codec_type"] == "video")
    audio = next(x for x in info["streams"] if x["codec_type"] == "audio")
    assert (video["width"], video["height"], video["codec_name"]) == (1080, 1920, "h264")
    assert audio["codec_name"] == "aac"
    subprocess.run(["ffmpeg", "-v", "error", "-i", str(output), "-f", "null", "-"], check=True)
