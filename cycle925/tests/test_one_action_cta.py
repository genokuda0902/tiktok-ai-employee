import sys,unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'src'))
from one_action_cta import *

class TestReviewOnlyCTA(unittest.TestCase):
 def test_10_genres(self):self.assertEqual(len(GENRES),10)
 def test_unique_topics(self):self.assertEqual(len({v['topic'] for v in GENRES.values()}),10)
 def test_safe_card(self):self.assertLess(CARD_RECT[3],SAFE_CAPTION_Y)
 def test_safe_geometry(self):self.assertTrue(validate_geometry())
 def test_scene_range(self):self.assertEqual(SCENE_END-SCENE_START,82)
 def test_policy(self):self.assertIn('PUBLICATION_NOT_APPROVED',POLICY)
 def test_stage_initial(self):self.assertEqual(stage_for_frame(0),0)
 def test_stage_mid(self):self.assertEqual(stage_for_frame(20),1)
 def test_stage_final(self):self.assertEqual(stage_for_frame(81),2)
 def test_stage_order(self):self.assertEqual(sorted(stage_for_frame(i) for i in range(82)),[0]*19+[1]*26+[2]*37)
 def test_smoothstep(self):self.assertEqual((smoothstep(-1),smoothstep(2)),(0.0,1.0))
 def test_no_external_media(self):self.assertTrue(all(v['topic'] for v in GENRES.values()))
 def test_rgb(self):self.assertEqual(blend_hex('#000000','#FFFFFF',0.5),(128,128,128))

if __name__=='__main__':unittest.main()
