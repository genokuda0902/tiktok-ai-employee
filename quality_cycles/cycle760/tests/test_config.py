import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

class JapaneseSubtitleConfigTests(unittest.TestCase):
    def test_srt_has_sixteen_cues(self):
        data=(ROOT/"config/phrase_cues.srt").read_text(encoding="utf-8")
        self.assertEqual(data.count(" --> "),16)

    def test_ten_genres(self):
        import json
        genres=json.loads((ROOT/"config/genres.json").read_text(encoding="utf-8"))["genres"]
        self.assertEqual(len(genres),10)
        self.assertEqual(len({x["name"] for x in genres}),10)

if __name__=="__main__":
    unittest.main()
