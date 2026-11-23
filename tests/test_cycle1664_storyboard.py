import unittest
from quality.cycle1664_storyboard import Scene, validate

class StoryboardTests(unittest.TestCase):
    def setUp(self):
        self.scenes=[Scene(0,4,"課題","毎日の集計"),Scene(4,8,"操作","AIに条件を渡す"),Scene(8,12,"確認","数字を確認")]
    def test_review_only_rejected(self):
        self.assertIn("missing_japanese_narration",validate(self.scenes,12))
    def test_overlapping_scene_rejected(self):
        scenes=[Scene(0,6,"A","字幕"),Scene(5,12,"B","字幕")]
        self.assertIn("invalid_timing",validate(scenes,12))
    def test_approved_passes(self):
        self.assertEqual([],validate(self.scenes,12,japanese_narration=True,sync_verified=True,asset_approved=True,employee_approved=True))
if __name__=="__main__": unittest.main()
