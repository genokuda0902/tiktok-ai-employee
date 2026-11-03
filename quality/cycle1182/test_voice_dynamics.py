import unittest
from voice_dynamics import audio_filter

class TestVoiceDynamics(unittest.TestCase):
    def test_default(self):
        self.assertIn('acompressor=', audio_filter())
        self.assertIn('alimiter=limit=0.89', audio_filter())
    def test_invalid(self):
        for kwargs in ({'highpass_hz':20},{'threshold':0},{'ratio':5},{'peak_limit':1.2}):
            with self.assertRaises(ValueError): audio_filter(**kwargs)

if __name__=='__main__':unittest.main()
