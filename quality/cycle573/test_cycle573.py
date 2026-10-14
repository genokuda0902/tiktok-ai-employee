import unittest
from render import VALUES,GENRES,CAPTION,calc,frame,validate_metadata

class TestCycle573(unittest.TestCase):
    def test_sum(self): self.assertEqual(calc(),720)
    def test_bad_values(self):
        for v in [(1,2,3),(-1,2,3,4),(1,2,3,True)]:
            with self.assertRaises(ValueError):calc(v)
    def test_ten_genres(self): self.assertEqual(len(GENRES),10)
    def test_all_genres_render(self):
        for g in GENRES: self.assertEqual(frame(1.1,g).size,(1080,1920))
    def test_beat_transitions(self):
        for t in [0,.94,.95,1.85,2.99]:self.assertEqual(frame(t).size,(1080,1920))
    def test_time_invalid(self):
        for t in [-.01,3.0]:
            with self.assertRaises(ValueError):frame(t)
    def test_bad_genre(self):
        with self.assertRaises(ValueError):frame(1,'unknown')
    def test_caption(self):self.assertIn('B2:B5',CAPTION)
    def test_publication_blocked(self):
        good={'publication':'NOT_APPROVED','auto_post':False,'rights':'REVIEW_ONLY_SYNTHETIC','synthetic':True,'narration':'ABSENT'}
        self.assertTrue(validate_metadata(good))
        for change in [{'publication':'APPROVED'},{'auto_post':True},{'rights':'UNKNOWN'},{'synthetic':False},{'narration':'VERIFIED'}]:
            bad={**good,**change}
            with self.assertRaises(ValueError):validate_metadata(bad)
if __name__=='__main__':unittest.main()