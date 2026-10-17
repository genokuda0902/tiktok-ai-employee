import unittest
from caption_beats import Beat, GENRES, validate_beats, at_time

class CaptionBeatTests(unittest.TestCase):
    def test_ten_genres(self):
        beats=[Beat(0,.7,"まだ手作業？","手作業"),Beat(.7,1.5,"AIで変わる","AI")]
        for genre in GENRES:
            self.assertTrue(validate_beats(beats,1.5,genre))
        self.assertEqual(at_time(beats,.7).text,"AIで変わる")
    def test_invalid_timeline(self):
        with self.assertRaises(ValueError):
            validate_beats([Beat(0,.5,"字幕","字幕"),Beat(.6,1.5,"次へ","次へ")],1.5,GENRES[0])

if __name__=="__main__":
    unittest.main()
