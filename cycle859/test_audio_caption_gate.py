import unittest,sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).parent))
from audio_caption_gate import coverage_from_rms

class TestAudioCaptionGate(unittest.TestCase):
    def test_full_coverage(self):
        self.assertEqual(coverage_from_rms([.1]*100,[{'start':0,'end':2}]),1)
    def test_half_coverage(self):
        self.assertEqual(coverage_from_rms([.1]*100,[{'start':0,'end':1}]),.5)
    def test_silence_ignored(self):
        self.assertEqual(coverage_from_rms([.1]*50+[0]*50,[{'start':0,'end':1}]),1)
    def test_no_voice_rejected(self):
        with self.assertRaises(ValueError):coverage_from_rms([0]*10,[{'start':0,'end':.2}])
    def test_invalid_caption(self):
        with self.assertRaises(ValueError):coverage_from_rms([.1]*10,[{'start':1,'end':.5}])
    def test_no_captions(self):
        with self.assertRaises(ValueError):coverage_from_rms([.1]*10,[])
    def test_invalid_threshold(self):
        with self.assertRaises(ValueError):coverage_from_rms([.1]*10,[{'start':0,'end':.2}],0)
if __name__=='__main__':unittest.main()
