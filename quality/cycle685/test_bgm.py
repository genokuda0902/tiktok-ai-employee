import tempfile,unittest,wave
from pathlib import Path
from make_bgm import synth_bgm
class Tests(unittest.TestCase):
    def test_stereo_duration(self):
        with tempfile.TemporaryDirectory() as d:
            with wave.open(str(synth_bgm(Path(d)/'a.wav')),'rb') as w:
                self.assertEqual(w.getnchannels(),2)
                self.assertEqual(w.getframerate(),48000)
                self.assertEqual(w.getnframes(),960000)
    def test_invalid(self):
        with self.assertRaises(ValueError): synth_bgm('x.wav',0)
