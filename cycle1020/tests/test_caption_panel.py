import sys
import tempfile
import unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'source'))
import caption_panel as c

class CaptionPanelTests(unittest.TestCase):
    def test_genres(self):
        self.assertEqual(len(c.GENRES),10)
        self.assertEqual(len(set(c.GENRES)),10)
    def test_stamp(self):
        self.assertAlmostEqual(c.stamp('00:00:02,900'),2.9)
        for value in ('00:70:00,000','99:01:90,000','2:3:4,5'):
            with self.assertRaises(ValueError):c.stamp(value)
    def test_srt_parse(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)/'x.srt'
            p.write_text('1\n00:00:00,000 --> 00:00:01,000\n前半です\n後半です\n\n2\n00:00:01,000 --> 00:00:02,000\n次の字幕\n次の行\n',encoding='utf-8')
            self.assertEqual(len(c.parse_srt(p)),2)
    def test_srt_gap_rejected(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)/'x.srt'
            p.write_text('1\n00:00:00,000 --> 00:00:01,000\n前半です\n後半です\n\n2\n00:00:01,300 --> 00:00:02,000\n次の字幕\n次の行\n',encoding='utf-8')
            with self.assertRaises(ValueError):c.parse_srt(p)
    def test_caption_layout_all_8(self):
        srt=Path(__file__).resolve().parents[1]/'fixtures'/'captions.srt'
        cues=c.parse_srt(srt)
        self.assertEqual(len(cues),8)
        for i,cue in enumerate(cues,1):
            self.assertEqual(c.card(cue['lines'],i,8).size,(1080,220))
    def test_too_long_line_rejected(self):
        with self.assertRaises(ValueError):c.card(['漢'*40,'後半です'],1,8)
    def test_fail_closed_without_review(self):
        with self.assertRaises(ValueError):c.validate('/missing','/tmp/x',[], 'ai_work',False,False)

if __name__=='__main__':unittest.main()
