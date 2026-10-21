import unittest
from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from scene03_contract import *

class Scene03ContractTest(unittest.TestCase):
    def test_geometry(self): self.assertTrue(validate())
    def test_ten_unique_themes(self): self.assertEqual(len(set(GENRES.values())),10)
    def test_first_phrase(self): self.assertEqual(speech_caption(6.0),"画面につなげば、")
    def test_second_phrase(self): self.assertEqual(speech_caption(7.0),"操作できる。")
    def test_speech_gate(self): self.assertEqual(speech_caption(7.8),"")
    def test_step_order(self): self.assertEqual([step(n) for n in (163,195,223)],[0,1,2])
    def test_safe_area(self): self.assertTrue(safe_caption_rect((55,1401,895,1580)))
    def test_unsafe_area(self): self.assertFalse(safe_caption_rect((55,1401,1050,1580)))
    def test_frame_bounds(self):
        with self.assertRaises(ValueError): step(245)
if __name__=="__main__": unittest.main()
