import sys
import unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).parent))
from task_cards import *

class TaskCardTests(unittest.TestCase):
    def test_genres(self):
        self.assertEqual(len(GENRES),10)
        for g in GENRES:
            self.assertTrue(validate_story(Story(g,'見つける',('作業一','作業二','作業三'),'行動しよう')))
    def test_invalid_genre(self):
        with self.assertRaises(ValueError):validate_story(Story('other','title',DEMO_TASKS,'cta'))
    def test_duplicate(self):
        with self.assertRaises(ValueError):validate_story(Story('ai_productivity','title',('同じ','同じ','別'),'cta'))
    def test_unsafe_copy(self):
        with self.assertRaises(ValueError):validate_story(Story('ai_productivity','title',('hello@example.com','ok','yes'),'cta'))
    def test_long_copy(self):
        with self.assertRaises(ValueError):validate_story(Story('ai_productivity','a'*25,DEMO_TASKS,'cta'))
    def test_bad_safe_area(self):
        with self.assertRaises(ValueError):validate_story(DEMO,caption_top=1800)
    def test_phase_before(self):
        self.assertEqual(card_phase(0,0)[0],0)
    def test_phase_order(self):
        self.assertGreater(card_phase(20,0)[0],0)
        self.assertEqual(card_phase(20,1)[0],0)
    def test_phase_end(self):
        self.assertEqual(card_phase(80,2)[1],0)
    def test_easing(self):
        self.assertEqual(ease_out(-1),0)
        self.assertEqual(ease_out(2),1)
    def test_caption_safe(self):
        im=draw_frame(50)
        self.assertEqual(im.size,(1080,1438))
        self.assertEqual(im.getpixel((100,1437))[3],0)
    def test_visual_progress(self):
        self.assertNotEqual(draw_frame(10).tobytes(),draw_frame(75).tobytes())
    def test_bounds(self):
        with self.assertRaises(ValueError):draw_frame(81)
    def test_manifest_fail_closed(self):
        import tempfile
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)/'source.mp4';p.write_bytes(b'test')
            m={**POLICY,'source_sha256':sha256(p)}
            self.assertTrue(validate_manifest(m,p))
            m['publication_approved']=True
            with self.assertRaises(ValueError):validate_manifest(m,p)
    def test_source_hash_gate(self):
        import tempfile
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)/'source.mp4';p.write_bytes(b'test')
            with self.assertRaises(ValueError):validate_manifest({**POLICY,'source_sha256':'0'*64},p)

if __name__=='__main__':unittest.main()
