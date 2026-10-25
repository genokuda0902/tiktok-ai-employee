"""No media/paid API required; deterministic CI contract tests."""
import unittest
from kinetic_action_cards import (GENRES,SCENES,EXAMPLES,POLICY,
                                  PANEL_TOP,PANEL_BOTTOM,PHOTO_BOTTOM,
                                  check_manifest,stamp,generate_ass)
class Tests(unittest.TestCase):
    def test_genres(self): self.assertEqual(len(GENRES),10)
    def test_duration(self): self.assertEqual(sum(SCENES),691)
    def test_timecode(self): self.assertEqual(stamp(691),'0:00:23.03')
    def test_examples(self): self.assertEqual(len(EXAMPLES),8)
    def test_safe_photo_region(self): self.assertLess(PANEL_TOP,PANEL_BOTTOM);self.assertLess(PANEL_BOTTOM,PHOTO_BOTTOM)
    def test_manifest(self): check_manifest(dict(POLICY),'ai_work')
    def test_fail_closed(self):
        for key in POLICY:
            m=dict(POLICY);m[key]=not m[key]
            with self.assertRaises(ValueError):check_manifest(m,'ai_work')
    def test_bad_genre(self):
        with self.assertRaises(ValueError):check_manifest(dict(POLICY),'unknown')
    def test_32_ass_events(self):self.assertEqual(generate_ass().count('Dialogue:'),32)
    def test_ten_genre_ass(self):
        for g in GENRES:self.assertEqual(generate_ass(g).count('Dialogue:'),32)
    def test_no_caption_overlap(self):self.assertLess(PANEL_BOTTOM,1300)
    def test_japanese_examples(self):
        self.assertTrue(all(any(ord(c)>127 for c in x) for x in EXAMPLES))
if __name__=='__main__':unittest.main()
