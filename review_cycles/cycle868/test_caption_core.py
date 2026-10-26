import unittest
from pathlib import Path
from caption_core import Beat, PANEL, GENRE_THEMES, build_ass, karaoke_tags, ass_time, beat_at, load_beats, validate_beats

BEATS = Path(__file__).with_name("caption_beats.json")
class CaptionTests(unittest.TestCase):
    def test_24_beats(self): self.assertEqual(len(load_beats(str(BEATS))), 24)
    def test_time(self): self.assertEqual(ass_time(23.03), "0:00:23.03")
    def test_karaoke_timing(self):
        import re
        x=karaoke_tags("こんにちは", 0.53)
        self.assertEqual(sum(map(int,re.findall(r"\\kf(\d+)",x))),53)
    def test_safe_panel(self):
        x,y,w,h=PANEL
        self.assertLess(x+w,1080);self.assertLess(y+h,1620)
    def test_out_of_order(self):
        with self.assertRaises(ValueError): validate_beats([Beat(0,1,"A"),Beat(.5,2,"B")])
    def test_empty(self):
        with self.assertRaises(ValueError): validate_beats([])
    def test_unsafe_text(self):
        with self.assertRaises(ValueError): validate_beats([Beat(0,1,"{\\bad}")])
    def test_unknown_genre(self):
        with self.assertRaises(ValueError): build_ass([Beat(0,1,"テスト")],genre="fake")
    def test_all_genres(self):
        for genre in GENRE_THEMES:
            with self.subTest(genre=genre):
                self.assertIn("Dialogue:",build_ass([Beat(0,1,"テスト")],genre=genre))
    def test_karaoke_count(self):
        beats=load_beats(str(BEATS)); ass=build_ass(beats)
        self.assertEqual(ass.count("Dialogue:"),len(beats))
        self.assertEqual(ass.count("\\kf"),sum(len(b.text) for b in beats))
    def test_beats_at_gaps(self):
        b=load_beats(str(BEATS))
        self.assertIsNone(beat_at(b,0.1));self.assertEqual(beat_at(b,0.5).text,"AIで仕事を")
    def test_ass_nonempty(self): self.assertGreater(len(build_ass(load_beats(str(BEATS)))),3000)
if __name__=="__main__": unittest.main()
