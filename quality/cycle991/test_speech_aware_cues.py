"""Offline unit tests for cycle991 speech-aware transition audio."""
import importlib.util
from array import array
from pathlib import Path
import unittest

module_path=Path(__file__).resolve().parent/'speech_aware_cues.py'
spec=importlib.util.spec_from_file_location('speech_aware_cues',module_path)
m=importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)

class TestCues(unittest.TestCase):
    def test_gain_lower_for_speech(self):
        self.assertLess(m.gain_for_voice(.16),m.gain_for_voice(.015))
    def test_gain_limits(self):
        self.assertEqual(m.gain_for_voice(0),.85)
        self.assertGreaterEqual(m.gain_for_voice(1),.18)
    def test_cue_envelope_edges(self):
        self.assertEqual(m.cue_sample(0,0,0),0)
        self.assertEqual(m.cue_sample(m.DURATION,0,0),0)
    def test_zero_boundaries_identity(self):
        src=array('h',[100]*100)
        out,events=m.process(src,())
        self.assertEqual(out,src);self.assertEqual(events,[])
    def test_one_event_no_clipping(self):
        src=array('h',[4000]*m.RATE)
        out,events=m.process(src,(15,))
        self.assertEqual(len(out),len(src))
        self.assertEqual(len(events),1)
        self.assertTrue(max(abs(v) for v in out)<32767)
        self.assertNotEqual(out,src)
    def test_bad_boundary_rejected(self):
        with self.assertRaises(ValueError):m.process(array('h',[0]*100),(90,))
    def test_reproducible(self):
        src=array('h',[1000]*m.RATE)
        self.assertEqual(m.process(src,(15,))[0],m.process(src,(15,))[0])

if __name__=='__main__':unittest.main()
