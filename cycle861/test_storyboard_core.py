import unittest,sys,json
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
from storyboard_core import *

class TestStoryboard(unittest.TestCase):
 def setUp(self):self.beats=json.loads((Path(__file__).parent/'caption_beats.json').read_text())
 def test_valid(self):self.assertTrue(validate_contract(self.beats))
 def test_ten_genres(self):self.assertEqual(len(GENRE_ACCENTS),10)
 def test_unique_colors(self):self.assertEqual(len(set(GENRE_ACCENTS.values())),10)
 def test_8_scenes(self):self.assertEqual(len(SCENES),8)
 def test_duration(self):self.assertEqual(FRAME_BOUNDARIES[-1],691)
 def test_timing_monotonic(self):self.assertTrue(all(b>a for a,b in zip(FRAME_BOUNDARIES,FRAME_BOUNDARIES[1:])))
 def test_caption_count(self):self.assertEqual(len(self.beats),24)
 def test_caption_no_overlap(self):self.assertTrue(all(a['end']<=b['start'] for a,b in zip(self.beats,self.beats[1:])))
 def test_subtitle_safe(self):self.assertLess(SUBTITLE_BOX[3],SAFE_CONTENT_BOTTOM)
 def test_output_review(self):self.assertIn('生成文の例（架空）',SCENES[4].card_title)
 def test_prompt_structure(self):self.assertTrue(all(any(w in x for x in SCENES[3].card_lines) for w in ['目的','相手','条件']))
 def test_correction_one(self):self.assertIn('1つずつ',SCENES[5].title[1])
 def test_template_fields(self):self.assertEqual(len(SCENES[6].card_lines),3)
 def test_not_claim_real_screenshot(self):self.assertTrue(all('実際のAI画面' not in ' '.join(s.card_lines) for s in SCENES))
 def test_video_size(self):self.assertEqual((WIDTH,HEIGHT),(1080,1920))
if __name__=='__main__':unittest.main()
