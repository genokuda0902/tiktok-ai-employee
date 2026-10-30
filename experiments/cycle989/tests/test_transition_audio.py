import math
import unittest
from array import array
from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from transition_audio import BOUNDARIES, SAMPLE_RATE, DURATION, effect_at, mix_samples

class TransitionAudioTest(unittest.TestCase):
    def test_zero_outside_effect(self):
        self.assertEqual(effect_at(-.1,DURATION),0)
        self.assertEqual(effect_at(DURATION,DURATION),0)
    def test_tapered_envelope(self):
        self.assertAlmostEqual(effect_at(0,DURATION),0)
        self.assertLess(abs(effect_at(DURATION-.0001,DURATION)),.001)
    def test_seven_boundaries_and_no_other_audio_changes(self):
        n=round(23.0*SAMPLE_RATE)
        source=array('h',[1234])*n
        mixed,events=mix_samples(source)
        self.assertEqual(len(events),7)
        self.assertEqual([x['frame'] for x in events],list(BOUNDARIES))
        self.assertEqual(source[0],mixed[0])
        self.assertEqual(source[100000],mixed[100000])
        self.assertNotEqual(source[round((87/30)*SAMPLE_RATE)],mixed[round((87/30)*SAMPLE_RATE)])
        self.assertEqual(source[-1],mixed[-1])
    def test_clip_protection(self):
        n=round(23*SAMPLE_RATE)
        with self.assertRaisesRegex(ValueError,'clipping'):
            mix_samples(array('h',[32760])*n)
    def test_invalid_rate(self):
        with self.assertRaises(ValueError):mix_samples(array('h',[0])*100,sample_rate=44100)
    def test_invalid_boundary(self):
        with self.assertRaises(ValueError):mix_samples(array('h',[0])*100000,boundaries=(87,))
    def test_synthetic_signal_bound(self):
        self.assertLessEqual(max(abs(effect_at(k/48000,DURATION)) for k in range(8880)),.021)

if __name__=='__main__':unittest.main()
