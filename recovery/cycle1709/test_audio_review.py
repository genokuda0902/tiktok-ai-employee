import unittest
from audio_review import command
class TestAudio(unittest.TestCase):
    def test_video_preserved(self):
        c=command('in.mp4','out.mp4'); self.assertEqual(c[c.index('-c:v')+1],'copy')
    def test_audio_required(self):
        self.assertIn('0:a:0',command('in.mp4','out.mp4'))
    def test_peak_target(self):
        self.assertIn('loudnorm=I=-16:TP=-1.5:LRA=7',command('in.mp4','out.mp4'))
if __name__=='__main__': unittest.main()
