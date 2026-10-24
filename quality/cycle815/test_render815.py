import json, tempfile, unittest
from pathlib import Path
from render815 import GENRE_ACCENTS, PHRASES, make_ass

class KaraokeTests(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory()
        self.root=Path(self.tmp.name)
        self.timing=self.root/'voice_timing.json'
        self.timing.write_text(json.dumps({'sentences':[
            {'text':''.join(p),'seconds':3.2291666} for p in PHRASES
        ]},ensure_ascii=False),encoding='utf-8')
    def tearDown(self): self.tmp.cleanup()
    def test_eight_scenes(self): self.assertEqual(len(PHRASES),8)
    def test_three_emphasis_states_each(self):
        dest=self.root/'out.ass';ends=make_ass(self.timing,dest)
        body=dest.read_text(encoding='utf-8')
        self.assertEqual(body.count('Dialogue: 0,'),24)
        self.assertEqual(body.count('Dialogue: 1,'),24)
        self.assertEqual(ends[-1],775)
    def test_uses_safe_zone(self):
        dest=self.root/'out.ass';make_ass(self.timing,dest)
        self.assertIn(r'\pos(540,1450)',dest.read_text(encoding='utf-8'))
    def test_ten_genre_settings(self): self.assertEqual(len(GENRE_ACCENTS),10)
    def test_mismatch_fails(self):
        data=json.loads(self.timing.read_text());data['sentences'][0]['text']='invalid'
        self.timing.write_text(json.dumps(data),encoding='utf-8')
        with self.assertRaises(AssertionError):make_ass(self.timing,self.root/'out.ass')

if __name__=='__main__': unittest.main()
