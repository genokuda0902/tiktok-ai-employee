from pathlib import Path
from unittest.mock import patch
from slide_legibility import render

def test_render_preserves_audio_and_subtitle_streams():
    with patch("subprocess.run") as run:
        render(Path("in.mp4"), Path("out.mp4"))
    args = run.call_args.args[0]
    assert args[args.index("-vf") + 1] == "eq=gamma=1.13:contrast=1.02:saturation=1.02"
    assert "0:a?" in args and "0:s?" in args
    assert args[args.index("-c:a") + 1] == "copy"
    assert args[args.index("-c:s") + 1] == "copy"
    assert args[args.index("-pix_fmt") + 1] == "yuv420p"
