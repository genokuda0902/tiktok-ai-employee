import json
import subprocess
import tempfile
import unittest
from pathlib import Path

import numpy as np
from clean_text_transitions import text_safe_cut, validate_plan, render


class CleanTextTransitionsTests(unittest.TestCase):
    def test_cut_never_doubles_text(self):
        a = np.zeros((16, 24, 3), dtype=np.uint8)
        b = np.full_like(a, 255)
        for fraction in [0, .25, .49, .5, .75, 1]:
            out = text_safe_cut(a, b, fraction)
            self.assertTrue(np.array_equal(out, a) or np.array_equal(out, b))

    def test_overlapping_windows_fail_closed(self):
        p = [dict(start=10, end=12, **{"from": 8, "to": 14}),
             dict(start=12, end=14, **{"from": 9, "to": 16})]
        with self.assertRaises(ValueError):
            validate_plan(p, 30, 100)

    def test_invalid_source_frames_fail_closed(self):
        with self.assertRaises(ValueError):
            validate_plan([dict(start=10, end=12, **{"from": 11, "to": 14})], 30, 100)

    def test_overlong_transition_fail_closed(self):
        with self.assertRaises(ValueError):
            validate_plan([dict(start=20, end=40, **{"from": 18, "to": 42})], 30, 100)

    def test_synthetic_video_smoke(self):
        with tempfile.TemporaryDirectory() as tmp:
            d = Path(tmp)
            source, out = d / "source.mp4", d / "out_REVIEW_ONLY.mp4"
            subprocess.run(["ffmpeg", "-hide_banner", "-loglevel", "error", "-y",
                            "-f", "lavfi", "-i", "color=c=navy:s=270x480:r=30:d=2",
                            "-f", "lavfi", "-i", "sine=frequency=440:duration=2",
                            "-shortest", "-c:v", "libx264", "-pix_fmt", "yuv420p",
                            "-c:a", "aac", str(source)], check=True)
            plan = d / "plan.json"
            plan.write_text(json.dumps([{"start": 11, "end": 14, "from": 9, "to": 16}]))
            report = render(source, out, plan, d / "frames")
            self.assertTrue(out.is_file() and out.stat().st_size > 1000)
            self.assertEqual(report["publication_approved"], False)
            streams = subprocess.check_output(["ffprobe", "-v", "error", "-show_entries",
                "stream=codec_type", "-of", "csv=p=0", str(out)], text=True)
            self.assertIn("video", streams)
            self.assertIn("audio", streams)


if __name__ == "__main__":
    unittest.main()
