import unittest
import numpy as np
from PIL import ImageChops
from prompt_legibility import (
    GENRES,PALETTES,POLICY,DEFAULT_CONTENT,draw_panel,validate_content,
    visible_chars,validate,sha256,compose_frame,SCENE_COVER
)

class PromptLegibilityTest(unittest.TestCase):
    def test_ten_distinct_genres(self):
        self.assertEqual(len(GENRES),10)
        self.assertEqual(len(set(PALETTES.values())),10)
    def test_all_genres_render(self):
        for g in GENRES:
            with self.subTest(genre=g):
                im=draw_panel(40,85,g)
                self.assertEqual(im.size,(908,758))
                self.assertIsNotNone(im.getbbox())
    def test_typing_monotonic(self):
        n=[visible_chars(i,85,DEFAULT_CONTENT) for i in range(85)]
        self.assertEqual(n,sorted(n))
        self.assertEqual(n[-1],sum(len(s) for s in DEFAULT_CONTENT['lines']))
    def test_dynamic_frame_change(self):
        a=draw_panel(0,85,'ai_work');b=draw_panel(65,85,'ai_work')
        self.assertIsNotNone(ImageChops.difference(a,b).getbbox())
    def test_full_mock_cover(self):
        frame=np.full((1920,1080,3),255,dtype=np.uint8)
        out=compose_frame(frame,draw_panel(40,85,'ai_work'))
        x0,y0,x1,y1=SCENE_COVER
        self.assertEqual(tuple(out[y0+10,x0+10]),(31,18,6))
        self.assertEqual(tuple(out[y1-10,x1-10]),(31,18,6))
        self.assertEqual(tuple(out[y0-1,x0]),(255,255,255))
    def test_invalid_genre(self):
        with self.assertRaises(ValueError):draw_panel(0,85,'unknown')
    def test_invalid_frame(self):
        with self.assertRaises(ValueError):draw_panel(85,85,'ai_work')
    def test_invalid_short_window(self):
        with self.assertRaises(ValueError):draw_panel(0,29,'ai_work')
    def test_content_schema(self):
        with self.assertRaises(ValueError):validate_content({'lines':['x'],'chips':['a','b','c']})
        with self.assertRaises(ValueError):validate_content({'lines':['a','b'],'chips':['a','b','c'],'extra':'x'})
        with self.assertRaises(ValueError):validate_content({'lines':['a\nb','c'],'chips':['a','b','c']})
        with self.assertRaises(ValueError):validate_content({'lines':['x'*17,'c'],'chips':['a','b','c']})
    def test_missing_source_fail_closed(self):
        with self.assertRaises(FileNotFoundError):validate('/not/exist.mp4','/tmp/new.mp4',POLICY,'ai_work',(0,60),DEFAULT_CONTENT)
    def test_review_policy_flags(self):
        self.assertFalse(POLICY['publication_approved'])
        self.assertFalse(POLICY['automatic_posting'])
        self.assertFalse(POLICY['external_upload'])
        self.assertFalse(POLICY['source_rights_reviewed'])
    def test_no_fake_product_claims(self):
        self.assertTrue(all('10倍' not in s and '秒で' not in s for s in DEFAULT_CONTENT['lines']))

if __name__=='__main__':unittest.main()
