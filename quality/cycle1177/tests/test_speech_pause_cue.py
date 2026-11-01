import sys,unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'code'))
from speech_pause_cue import *

class PauseCueTests(unittest.TestCase):
    def test_parse(self):
        self.assertEqual(parse_silences('silence_start: 1.2\nsilence_end: 1.65'),[(1.2,1.65)])
    def test_unmatched_end(self):self.assertEqual(parse_silences('silence_end: 1.5'),[])
    def test_unmatched_start(self):self.assertEqual(parse_silences('silence_start: 1.5'),[])
    def test_chapters(self):
        self.assertEqual(select_cues([(0,3),(3,6)],[(1.2,1.6),(4.3,4.8)]),[1.625,4.825])
    def test_outro_excluded(self):self.assertEqual(select_cues([(0,3)],[(2.6,2.95)]),[])
    def test_short_excluded(self):self.assertEqual(select_cues([(0,3)],[(1.3,1.4)]),[])
    def test_midpoint(self):
        self.assertEqual(select_cues([(0,5)],[(.6,1.0),(2.1,2.5)]),[2.525])
    def test_alpha(self):
        self.assertEqual(pulse_alpha(0,0),0)
        self.assertGreater(pulse_alpha(.18,0),.99)
        self.assertEqual(pulse_alpha(.36,0),0)
    def test_bad_duration(self):
        with self.assertRaises(ValueError):pulse_alpha(.1,0,-1)
    def test_ten_genres(self):self.assertEqual(len(GENRES),10)
    def test_rgba(self):self.assertEqual(rgba_color('#00ffcc',100),(0,255,204,100))
    def test_transparency(self):self.assertIsNone(cue_frame('#55ccaa',0).getbbox())
    def test_visible(self):self.assertIsNotNone(cue_frame('#55ccaa',1).getbbox())
    def test_bad_strength(self):
        with self.assertRaises(ValueError):cue_frame('#55ccaa',1.5)
    def test_safe_area(self):
        m={'streams':[{'codec_type':'video','width':1080,'height':1920,'nb_frames':'675'},
                      {'codec_type':'audio','codec_name':'aac'}]}
        self.assertEqual(validate_source(m,'ai'),675)
        with self.assertRaises(ValueError):validate_source(m,'ai',(200,1510))
        with self.assertRaises(ValueError):validate_source(m,'unknown')
    def test_bad_resolution(self):
        m={'streams':[{'codec_type':'video','width':720,'height':1280,'nb_frames':'675'},
                      {'codec_type':'audio','codec_name':'aac'}]}
        with self.assertRaises(ValueError):validate_source(m,'ai')
if __name__=='__main__':unittest.main()
