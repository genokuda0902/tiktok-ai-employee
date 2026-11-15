import unittest
from unittest.mock import patch
from process import peak_guard

class PeakGuardTest(unittest.TestCase):
    def test_invalid_limit(self):
        with self.assertRaises(ValueError): peak_guard('a.mp4','b.mp4',1.0)
    @patch('subprocess.run')
    def test_video_copy_and_audio_filter(self, run):
        peak_guard('a.mp4','/tmp/b.mp4')
        cmd=run.call_args.args[0]
        self.assertEqual(cmd[cmd.index('-c:v')+1],'copy')
        self.assertIn('alimiter=limit=0.68',cmd[cmd.index('-af')+1])
        self.assertTrue(run.call_args.kwargs['check'])
if __name__=='__main__': unittest.main()
