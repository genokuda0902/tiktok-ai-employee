import unittest
from quality.cycle1586_audio_gate import publishable
class TestGate(unittest.TestCase):
    def test_silent_fails(self):
        self.assertFalse(publishable({"width":720,"height":1280,"audio_streams":0},True,True,True,True))
    def test_electronic_tone_not_speech(self):
        self.assertFalse(publishable({"width":720,"height":1280,"audio_streams":1},False,True,True,True))
    def test_requires_approval(self):
        self.assertFalse(publishable({"width":720,"height":1280,"audio_streams":1},True,True,True,False))
if __name__ == "__main__": unittest.main()
