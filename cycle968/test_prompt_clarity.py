import unittest
from prompt_clarity import WIDTH,CAPTION_TOP,GENRES,draw_scene,assert_review_genre,SCENE_START,SCENE_END
import numpy as np

class PromptClarityTests(unittest.TestCase):
    def test_ten_genres(self): self.assertEqual(len(GENRES),10)
    def test_only_reviewed_genre(self):
        for g in GENRES:
            if g=='ai_work':assert_review_genre(g)
            else:
                with self.assertRaises(PermissionError):assert_review_genre(g)
    def test_unknown_rejected(self):
        with self.assertRaises(ValueError):assert_review_genre('unknown')
    def test_scene_87_frames(self): self.assertEqual(SCENE_END-SCENE_START,87)
    def test_geometry(self): self.assertEqual(draw_scene(0).shape,(CAPTION_TOP,WIDTH,3))
    def test_three_progress_states_are_distinct(self):
        a,b,c=[draw_scene(p) for p in (0.05,.45,.8)]
        self.assertGreater(np.mean(np.abs(a.astype('int16')-b.astype('int16'))),1.0)
        self.assertGreater(np.mean(np.abs(b.astype('int16')-c.astype('int16'))),1.0)
    def test_caption_region_not_drawn(self):self.assertLess(draw_scene(.5).shape[0],1920)
    def test_no_private_images_or_network(self):
        import inspect,prompt_clarity
        s=inspect.getsource(prompt_clarity)
        self.assertNotIn('requests.',s);self.assertNotIn('IMG_5805',s)

if __name__=='__main__':unittest.main()
