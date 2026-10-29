import unittest
from quality.cycle960.safe_caption import ACCENTS, CUTS, SCENES, SAFE_RIGHT, SAFE_BOTTOM, scene_at_frame, panel_for_scene

class TestSafeCaption(unittest.TestCase):
 def test_ten_genres(self):
  self.assertEqual(len(ACCENTS),10)
 def test_all_eight_scenes_in_all_genres(self):
  for genre in ACCENTS:
   for scene in range(8):
    with self.subTest(genre=genre,scene=scene):
     im,boxes=panel_for_scene(scene,genre)
     self.assertEqual(im.size,(1080,405))
     self.assertTrue(boxes)
     self.assertTrue(all(x0>=78 and x1<=858 and y1<=1640 for x0,y0,x1,y1 in boxes))
 def test_cut_boundaries(self):
  for i in range(8):
   self.assertEqual(scene_at_frame(CUTS[i]),i)
   self.assertEqual(scene_at_frame(CUTS[i+1]-1),i)
 def test_invalid_frame(self):
  for f in (-1,691):
   with self.assertRaises(ValueError):scene_at_frame(f)
 def test_safe_insets(self):
  self.assertLessEqual(883,SAFE_RIGHT)
  self.assertLessEqual(1618,SAFE_BOTTOM)
 def test_japanese_caption_text_preserved(self):
  expected=("AIで仕事を早くするなら、最初の一歩が大事。","まず、繰り返している作業を書き出す。",
    "次に、完成形の見本を用意する。","指示は、目的と条件を具体的に伝える。",
    "最初の出力は、必ず自分で確かめる。","違いがあれば、修正点を一つずつ伝える。",
    "使える指示は、テンプレートに残す。","小さな時短を、毎日の習慣にしよう。")
  for i,scene in enumerate(SCENES):
   self.assertEqual("".join(t for line in scene for t,_ in line),expected[i])
 def test_invalid_genre(self):
  with self.assertRaises(ValueError):panel_for_scene(0,"unknown")
if __name__=="__main__":unittest.main()
