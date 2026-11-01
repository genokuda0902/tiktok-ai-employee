import sys
import unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
from voice_presence import GENRES,FILTER,render,validate_source

class VoicePresenceTests(unittest.TestCase):
    def test_ten_genres(self): self.assertEqual(len(GENRES),10)
    def test_genres_unique(self): self.assertEqual(len(set(GENRES)),10)
    def test_no_music(self): self.assertNotIn('amix',FILTER)
    def test_highpass(self): self.assertIn('highpass=f=80',FILTER)
    def test_mild_presence(self): self.assertIn('g=1.3',FILTER)
    def test_fail_unknown_genre(self):
        with self.assertRaises(ValueError): render('absent.mp4','out.mp4','unknown')
    def test_fail_missing_source(self):
        with self.assertRaises(FileNotFoundError): validate_source('not_real.mp4')
    def test_fail_same_file(self):
        with self.assertRaises(ValueError): render('x.mp4','x.mp4')
    def test_fail_existing_output(self):
        with self.assertRaises(ValueError): render('x.mp4',__file__)

if __name__=='__main__': unittest.main()
