import json,unittest
from pathlib import Path
DATA=json.loads(Path(__file__).with_name("storyboard.json").read_text())
class TestStoryboard(unittest.TestCase):
 def test_genres(self):self.assertEqual(len(set(DATA["genres"])),10)
 def test_scenes(self):self.assertEqual(len(DATA["scenes"]),7)
 def test_narration_required(self):self.assertTrue(DATA["narration_required"])
 def test_no_publishing(self):self.assertFalse(DATA["auto_post"])
 def test_not_approved(self):self.assertEqual(DATA["publication"],"NOT_APPROVED")
 def test_dimensions(self):self.assertEqual(DATA["video_size"],[1080,1920])
 def test_japanese_subtitles(self):self.assertTrue(all(any(ord(c)>0x3000 for c in s[1]) for s in DATA["scenes"]))
if __name__=="__main__":unittest.main()
