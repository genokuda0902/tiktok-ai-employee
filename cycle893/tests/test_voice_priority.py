import math
import sys
import tempfile
import unittest
import wave
from array import array
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'src'))
from voice_priority import RATE, gain_envelope, mix, read_mono_pcm16


def wav(path, samples, rate=RATE, channels=1):
    with wave.open(str(path), 'wb') as w:
        w.setnchannels(channels)
        w.setsampwidth(2)
        w.setframerate(rate)
        w.writeframes(array('h', samples).tobytes())


class VoicePriorityTests(unittest.TestCase):
    def test_duck_speech_keep_quiet(self):
        n = RATE * 2
        v = array('h', [0] * n)
        c = array('h', [1500] * n)
        for i in range(RATE//2, RATE*3//2):
            v[i] = int(12000 * math.sin(2*math.pi*200*i/RATE))
        gains, rms = gain_envelope(v, c)
        self.assertLess(gains[90], 0.30)
        self.assertGreater(gains[10], 0.95)
        self.assertGreater(gains[-1], 0.95)
        self.assertGreater(rms[90], 0.025)

    def test_validation(self):
        v = array('h', [0]*RATE)
        with self.assertRaises(ValueError):
            gain_envelope(v, array('h', [0]*(RATE*2)))
        with self.assertRaises(ValueError):
            gain_envelope(v, v, min_gain=0)
        with self.assertRaises(ValueError):
            gain_envelope(v, v, threshold=-1)
        with self.assertRaises(ValueError):
            gain_envelope(array('h',[0]*100), array('h',[0]*100))

    def test_reject_wrong_format(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)/'bad.wav'
            wav(p,[0]*RATE,rate=44100)
            with self.assertRaises(ValueError):
                read_mono_pcm16(p)

    def test_end_to_end(self):
        with tempfile.TemporaryDirectory() as d:
            d=Path(d)
            n=RATE*2
            v=[int(9000*math.sin(2*math.pi*200*i/RATE)) if i<RATE else 0 for i in range(n)]
            c=[500 if i%2 else -500 for i in range(n)]
            wav(d/'v.wav',v)
            wav(d/'c.wav',c)
            m=mix(d/'v.wav',d/'c.wav',d/'out.wav')
            self.assertEqual(m['samples'],n)
            self.assertLess(m['speech_overlap_cue_energy_reduction_db'],-9)
            self.assertGreater(m['quiet_cue_mean_gain'],0.90)
            self.assertTrue((d/'out.wav').is_file())


if __name__=='__main__':
    unittest.main()
