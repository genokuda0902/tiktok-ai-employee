import unittest
from voice_gate import japanese_voice_ready

class VoiceGateTest(unittest.TestCase):
    def test_return_type(self):
        self.assertIsInstance(japanese_voice_ready(),bool)

if __name__=='__main__': unittest.main()
