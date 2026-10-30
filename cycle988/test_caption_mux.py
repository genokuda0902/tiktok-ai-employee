import json
import tempfile
import unittest
from pathlib import Path
from caption_mux import GENRES, fmt, make_srt, validate, render

class CaptionMuxTest(unittest.TestCase):
    def setUp(self):
        self.manifest=json.loads((Path(__file__).parent/'captions_ai_work.json').read_text(encoding='utf-8'))
    def test_ten_genres(self):
        self.assertEqual(len(GENRES),10)
    def test_other_nine_fail_closed(self):
        for genre in GENRES[1:]:
            with self.assertRaisesRegex(ValueError,'fail closed'):
                validate(self.manifest,23.033333,genre)
    def test_unknown_genre(self):
        with self.assertRaises(ValueError):
            validate(self.manifest,23.033333,'unknown')
    def test_eight_cues(self):
        self.assertEqual(len(validate(self.manifest,23.033333,'ai_work')),8)
    def test_overlap_rejected(self):
        bad=json.loads(json.dumps(self.manifest))
        bad['cues'][1]['start']=2.8
        with self.assertRaisesRegex(ValueError,'Overlapping'):
            validate(bad,23.033333,'ai_work')
    def test_empty_rejected(self):
        bad=json.loads(json.dumps(self.manifest))
        bad['cues'][0]['text']=''
        with self.assertRaises(ValueError):
            validate(bad,23.033333,'ai_work')
    def test_out_of_range(self):
        bad=json.loads(json.dumps(self.manifest))
        bad['cues'][-1]['end']=26
        with self.assertRaises(ValueError):
            validate(bad,23.033333,'ai_work')
    def test_coverage(self):
        bad=json.loads(json.dumps(self.manifest))
        bad['cues'][-1]['end']=22.8
        with self.assertRaisesRegex(ValueError,'coverage'):
            validate(bad,23.033333,'ai_work')
    def test_japanese_srt(self):
        s=make_srt(self.manifest['cues'])
        self.assertIn('00:00:02,900',s)
        self.assertIn('小さな時短を',s)
        self.assertEqual(s.count('-->'),8)
    def test_timestamp(self):
        self.assertEqual(fmt(23.033333),'00:00:23,033')
    def test_no_overwrite(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)/'input.mp4'
            p.write_bytes(b'dummy')
            m=Path(d)/'manifest.json'
            m.write_text('{}')
            with self.assertRaisesRegex(ValueError,'overwrite'):
                render(p,p,m,d,synthetic=True)

if __name__=='__main__':
    unittest.main()
