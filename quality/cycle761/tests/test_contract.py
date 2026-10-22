import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
import cycle761_endcard as endcard

class TestEndcard(unittest.TestCase):
    def test_genres(self):
        self.assertEqual(len(endcard.GENRES), 10)

    def test_config(self):
        config = json.loads((ROOT / "config/ai_work_endcard.json").read_text(encoding="utf-8"))
        self.assertEqual(endcard.validate(config)["genre"], "ai_work")

    def test_unapproved_asset_rejected(self):
        config = json.loads((ROOT / "config/ai_work_endcard.json").read_text(encoding="utf-8"))
        config["asset_rights"] = "unknown"
        with self.assertRaises(ValueError):
            endcard.validate(config)

    def test_layout(self):
        self.assertEqual((endcard.W, endcard.H, endcard.FPS), (1080, 1920, 30))
        self.assertLessEqual(861, endcard.RIGHT_SAFE)
        self.assertEqual(endcard.CUT_FRAME + endcard.END_FRAMES, 819)
