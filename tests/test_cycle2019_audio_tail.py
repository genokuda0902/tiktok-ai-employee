import unittest
from tools.cycle2019_audio_tail import render
class TestAudioOutro(unittest.TestCase):
    def test_invalid_fade(self):
        from unittest.mock import patch
        with patch("tools.cycle2019_audio_tail.probe",return_value={"format":{"duration":"5.0"}}):
            with self.assertRaises(ValueError):
                render("in.mp4","out.mp4",6.0)
if __name__=="__main__": unittest.main()
