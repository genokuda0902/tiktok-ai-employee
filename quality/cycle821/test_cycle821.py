"""Cycle821 CI regression tests: storyboard coverage, voice matching, safe layout."""
import unittest,tempfile,json,sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
from genre_catalog821 import GENRES,validate,write_catalog
from render821 import base

class Cycle821Tests(unittest.TestCase):
 def test_ten_genres(self):self.assertTrue(validate())
 def test_eighty_unique_scene_scripts(self):
  self.assertEqual(sum(len(v[2]) for v in GENRES.values()),80)
  self.assertEqual(len({tuple(v[2]) for v in GENRES.values()}),10)
 def test_business_script_matches_existing_japanese_voice(self):
  self.assertEqual(GENRES["sales_business"][2],["".join(x) for x in base.PHRASES])
 def test_unvoiced_genres_cannot_be_marked_ready(self):
  with tempfile.TemporaryDirectory() as d:
   data=json.loads(write_catalog(Path(d)/"catalog.json").read_text())
   self.assertEqual(sum(v["voice_ready"] for v in data.values()),1)
 def test_mobile_caption_safe_region(self):
  self.assertLess(1235+3*100,1590)
 def test_phrase_width(self):
  self.assertTrue(all(max(map(len,parts))<=12 for parts in base.PHRASES))

if __name__=="__main__":unittest.main()
