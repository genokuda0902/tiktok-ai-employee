"""Zero-cost 10-genre scene-summary QA tests."""
import copy
import json
import unittest
from pathlib import Path
from render_summary_captions import GENRES,validate,build_ass,timestamp
CFG=json.loads((Path(__file__).parent/'config.json').read_text(encoding='utf-8'))
class Contract(unittest.TestCase):
    def test_valid(self): self.assertTrue(validate(CFG))
    def test_all_ten_genres(self):
        for genre in GENRES:
            cfg=copy.deepcopy(CFG);cfg['genre']=genre
            with self.subTest(genre=genre):self.assertTrue(validate(cfg))
    def test_fail_closed_publication(self):
        for key in ('publication_approved','rights_reviewed'):
            cfg=copy.deepcopy(CFG);cfg[key]=True
            with self.assertRaises(ValueError):validate(cfg)
    def test_no_transcript_claim(self):
        cfg=copy.deepcopy(CFG);cfg['subtitle_kind']='verified_transcript'
        with self.assertRaises(ValueError):validate(cfg)
    def test_cue_overlap_rejected(self):
        cfg=copy.deepcopy(CFG);cfg['cues'][2]['start']=2.0
        with self.assertRaises(ValueError):validate(cfg)
    def test_cue_gap_rejected(self):
        cfg=copy.deepcopy(CFG);cfg['cues'][1]['start']=1.6
        with self.assertRaises(ValueError):validate(cfg)
    def test_too_long_line_rejected(self):
        cfg=copy.deepcopy(CFG);cfg['cues'][0]['text']='あ'*30
        with self.assertRaises(ValueError):validate(cfg)
    def test_ass_injection_rejected(self):
        cfg=copy.deepcopy(CFG);cfg['cues'][0]['text']='\\Nbad'
        with self.assertRaises(ValueError):validate(cfg)
    def test_safe_zone_change_rejected(self):
        cfg=copy.deepcopy(CFG);cfg['safe_area']['bottom_px']=1850
        with self.assertRaises(ValueError):validate(cfg)
    def test_duration_ends_at_video(self):
        cfg=copy.deepcopy(CFG);cfg['cues'][-1]['end']=22
        with self.assertRaises(ValueError):validate(cfg)
    def test_ass_cues(self):
        ass=build_ass(CFG)
        self.assertEqual(ass.count('Dialogue:'),9)
        self.assertIn('Noto Sans CJK JP',ass)
        self.assertIn('手作業の集計',ass)
        self.assertIn('0:00:23.84',ass)
    def test_timestamp(self):self.assertEqual(timestamp(23.843),'0:00:23.84')
if __name__=='__main__':unittest.main()
