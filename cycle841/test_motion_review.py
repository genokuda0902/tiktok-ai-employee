import unittest
from pathlib import Path
from cycle841 import motion_review as m

class TestMotionReview(unittest.TestCase):
    def setUp(self):
        self.good={**m.REQUIRED,'contains_confidential_media':False,'source_sha256':'a'*64}
    def test_ten_genres(self):
        self.assertEqual(len(set(m.GENRES)),10)
        for genre in m.GENRES:
            m.validate_manifest(self.good,genre)
    def test_unknown_genre_rejected(self):
        with self.assertRaises(ValueError): m.validate_manifest(self.good,'not_a_genre')
    def test_reject_private_media(self):
        for bad in ({'contains_confidential_media':True}, {'contains_personal_data':True},
                    {'publication_approved':True}, {'automatic_posting':True},
                    {'external_upload':True}, {'review_only':False},
                    {'source_rights_reviewed':True}):
            with self.subTest(bad=bad),self.assertRaises(ValueError):
                m.validate_manifest({**self.good,**bad},'ai_work')
    def test_reject_missing_source_pin(self):
        with self.assertRaises(ValueError):
            m.validate_manifest({**self.good,'source_sha256':'oops'},'ai_work')
    def test_scene_accounting(self):
        self.assertEqual(sum(m.SCENE_FRAMES),691)
        self.assertEqual(m.ranges(),[(89,170),(422,511),(588,691)])
    def test_motion_only_visual_area(self):
        x,y,w,h=m.REGION
        self.assertGreaterEqual(x,40)
        self.assertGreaterEqual(y,330)
        self.assertLessEqual(y+h,1200) # burned captions begin below
        self.assertLessEqual(x+w,1080)
    def test_motion_filter(self):
        f=m.filtergraph()
        for a,b in m.ranges():
            self.assertIn(f'between(on,{a},{b-1})',f)
            self.assertIn(f'between(n,{a},{b-1})',f)
        self.assertIn('zoompan=',f)
        self.assertIn('overlay=',f)
    def test_no_silent_audio_replacement(self):
        self.assertIn("'-c:a','copy'",Path(m.__file__).read_text())

if __name__=='__main__': unittest.main()
