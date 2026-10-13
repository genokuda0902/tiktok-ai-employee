import unittest
GENRES = ['AI・仕事効率化','美容・身だしなみ','恋愛・心理','お金・節約','営業・ビジネス','転職・キャリア','健康・生活改善','雑学・科学','旅行・グルメ','商品比較・暮らし']
W,H,FPS=1080,1920,30
START_FRAME,COUNT,Y0,Y1=280,55,515,1098
PRESET={'effect':'material_light_pass','max_alpha':135,'safe_subtitle_top':1100,'publication':'NOT_APPROVED'}
class TestCycle557(unittest.TestCase):
 def test_genres(self): self.assertEqual(len(set(GENRES)),10)
 def test_vertical(self): self.assertEqual((W,H,FPS),(1080,1920,30))
 def test_timing(self): self.assertGreaterEqual(START_FRAME,275); self.assertLessEqual(START_FRAME+COUNT,336)
 def test_subtitle_safe(self): self.assertLess(Y1,PRESET['safe_subtitle_top'])
 def test_alpha(self): self.assertLessEqual(PRESET['max_alpha'],135)
 def test_not_published(self): self.assertEqual(PRESET['publication'],'NOT_APPROVED')
 def test_effect(self): self.assertEqual(PRESET['effect'],'material_light_pass')
if __name__=='__main__': unittest.main()
