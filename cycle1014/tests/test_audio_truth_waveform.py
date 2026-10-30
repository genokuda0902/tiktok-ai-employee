import importlib.util
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

MODULE=Path(__file__).resolve().parents[1]/'source'/'audio_truth_waveform.py'
spec=importlib.util.spec_from_file_location('audio_truth_waveform',MODULE)
m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)

class QualityTests(unittest.TestCase):
    def test_ten_genres(self):
        self.assertEqual(len(m.GENRES),10)
        self.assertEqual(len(set(m.GENRES)),10)
    def test_waveform_bar_bounds(self):
        self.assertEqual(m.bar_height(-100),3)
        self.assertEqual(m.bar_height(20),58)
        self.assertGreater(m.bar_height(-15),m.bar_height(-40))
    def test_srt_cues(self):
        self.assertEqual(m.parse_srt('1\n00:00:00,000 --> 00:00:02,900\n日本語'),[(0,2.9)])
    def test_cue_signal_fraction(self):
        self.assertEqual(m.cue_activity([-50,-30,-30,-50],[(0,4/30)])[0]['audio_signal_fraction'],.5)
    def test_empty_cue_rejected(self):
        with self.assertRaises(ValueError):m.cue_activity([-20],[(5,6)])
    def test_unknown_genre_rejected(self):
        with tempfile.TemporaryDirectory() as d:
            source=Path(d)/'source.mp4';source.write_bytes(b'foo')
            with self.assertRaises(ValueError):m.validate(source,Path(d)/'out.mp4','bad',True)
    def test_not_review_only_rejected(self):
        with tempfile.TemporaryDirectory() as d:
            source=Path(d)/'source.mp4';source.write_bytes(b'foo')
            with self.assertRaises(ValueError):m.validate(source,Path(d)/'out.mp4','ai_work',False)
    def test_private_sha_rejected(self):
        with tempfile.TemporaryDirectory() as d:
            source=Path(d)/'source.mp4';source.write_bytes(b'foo')
            fake={'streams':[{'codec_type':'video','codec_name':'h264','width':1080,'height':1920,'r_frame_rate':'30/1','nb_frames':'60'}, {'codec_type':'audio','codec_name':'aac','sample_rate':'48000','tags':{'language':'jpn'}}], 'format':{'duration':'2'}}
            with patch.object(m,'probe',return_value=fake):
                with self.assertRaises(ValueError):m.validate(source,Path(d)/'out.mp4','ai_work',True)
                with self.assertRaises(ValueError):m.validate(source,Path(d)/'out.mp4','ai_work',False)
    def test_render_overlay(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)/'frame.png';m.draw_wave(p,[-40,-15]*30,47,60)
            from PIL import Image
            im=Image.open(p)
            self.assertEqual(im.size,(940,136))
            self.assertEqual(im.getpixel((5,5))[3],255)

if __name__=='__main__':unittest.main()
