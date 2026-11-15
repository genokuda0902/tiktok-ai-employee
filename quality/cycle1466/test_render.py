import json, unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parent
class Tests(unittest.TestCase):
 def test_caption_timing(self):
  c=json.loads((ROOT/'captions.json').read_text());self.assertEqual(len(c),4)
  self.assertEqual([(x['start'],x['end']) for x in c],[(0,3),(3,6),(6,9),(9,12)])
 def test_no_false_spoken_claim(self):
  self.assertTrue(all(not x['spoken'] for x in json.loads((ROOT/'captions.json').read_text())))
 def test_fail_closed(self):
  q=json.loads((ROOT/'qa.json').read_text());self.assertFalse(all(q.values()))
if __name__=='__main__':unittest.main()
