import unittest
from cycle553_renderer import valid_scene, render_frame, ease, probe

class TestResultFirstHook(unittest.TestCase):
    def test_truth(self): self.assertTrue(valid_scene([120,150,200,250],720,'この集計、まだ手入力？'))
    def test_false_claim_rejected(self):
        with self.assertRaises(ValueError):valid_scene([1,2],99,'OK')
    def test_negative_rejected(self):
        with self.assertRaises(ValueError):valid_scene([1,-2],-1,'OK')
    def test_empty_rejected(self):
        with self.assertRaises(ValueError):valid_scene([],0,'OK')
    def test_overlong_rejected(self):
        with self.assertRaises(ValueError):valid_scene([1],1,'長'*23)
    def test_ease_bounds(self):
        self.assertEqual(ease(-2),0);self.assertEqual(ease(2),1)
    def test_first_frame(self):self.assertEqual(render_frame(0).size,(540,960))
    def test_last_hook_frame(self):self.assertEqual(render_frame(2.39).size,(540,960))
    def test_generic_genre(self):self.assertTrue(valid_scene([3,4],7,'料理の材料、数えた？'))

if __name__=='__main__':unittest.main()
