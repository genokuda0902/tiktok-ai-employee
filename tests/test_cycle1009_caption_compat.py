import sys,unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'tools'/'quality'))
from cycle1009_caption_compat import GENRES,srt_to_vtt,process
SRT='1\n00:00:00,100 --> 00:00:00,900\n日本語字幕\n\n2\n00:00:01,000 --> 00:00:01,900\n次の字幕\n'
class CaptionCompatibilityTest(unittest.TestCase):
    def test_ten_genres(self): self.assertEqual(len(GENRES),10)
    def test_japanese_vtt(self):
        v=srt_to_vtt(SRT)
        self.assertIn('WEBVTT',v);self.assertIn('日本語字幕',v)
        self.assertIn('00:00:00.100 --> 00:00:00.900',v)
    def test_empty_rejected(self):
        with self.assertRaises(ValueError): srt_to_vtt('')
    def test_overlap_rejected(self):
        with self.assertRaises(ValueError): srt_to_vtt(SRT.replace('00:00:01,000','00:00:00,800'))
    def test_reversed_rejected(self):
        with self.assertRaises(ValueError): srt_to_vtt(SRT.replace('00:00:00,900','00:00:00,050'))
    def test_invalid_minutes_rejected(self):
        with self.assertRaises(ValueError): srt_to_vtt(SRT.replace('00:00:00,900','00:61:00,900'))
    def test_invalid_number_rejected(self):
        with self.assertRaises(ValueError): srt_to_vtt(SRT.replace('\n2\n','\n4\n'))
    def test_unknown_genre_rejected(self):
        with self.assertRaises(ValueError):
            process(Path('/no.mp4'),Path('/out.mp4'),Path('/no.srt'),genre='unknown')
    def test_missing_source_rejected(self):
        with self.assertRaises(FileNotFoundError):
            process(Path('/no.mp4'),Path('/out.mp4'),Path('/no.srt'),genre='business')
if __name__=='__main__': unittest.main()
