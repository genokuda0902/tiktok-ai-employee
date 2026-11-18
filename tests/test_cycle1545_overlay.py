import importlib.util
import unittest
from pathlib import Path

PATH = Path(__file__).resolve().parents[1] / "tools" / "cycle1545_overlay.py"
spec = importlib.util.spec_from_file_location("cycle1545_overlay", PATH)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


class TestTimedOverlays(unittest.TestCase):
    def test_four_distinct_stages(self):
        self.assertEqual(len(module.STEPS), 4)
        self.assertEqual([(s, e) for _, s, e in module.STEPS],
                         [(0, 3), (3, 6), (6, 9), (9, 12)])

    def test_review_only_and_no_narration_claim(self):
        filt = module.build_filter()
        self.assertIn("REVIEW ONLY", filt)
        self.assertIn("音声未完成", filt)
        self.assertIn("SUM関数", filt)

    def test_missing_input_rejected(self):
        with self.assertRaises(FileNotFoundError):
            module.render("/does-not-exist.mp4", "/tmp/never.mp4")


if __name__ == "__main__":
    unittest.main()
