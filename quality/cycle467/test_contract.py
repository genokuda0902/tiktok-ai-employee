import json
import unittest
from pathlib import Path
from quality_contract import validate, caption_safe

class QualityTests(unittest.TestCase):
    def test_scene_plan(self):
        plan = json.loads(Path(__file__).with_name('scene_plan.json').read_text(encoding='utf-8'))
        self.assertTrue(validate(plan))
    def test_caption_geometry(self):
        self.assertTrue(caption_safe((40, 1005, 680, 1115)))
        self.assertFalse(caption_safe((40, 1180, 680, 1270)))

if __name__ == '__main__':
    unittest.main()
