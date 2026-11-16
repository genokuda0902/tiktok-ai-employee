import unittest
from unittest.mock import patch
from process import export

class TestExport(unittest.TestCase):
    def test_reject_invalid_crf(self):
        with self.assertRaises(ValueError): export('a.mp4','b.mp4',-1)
    @patch('process.subprocess.run')
    def test_quality_and_audio_copy(self, run):
        export('a.mp4','b.mp4')
        cmd=run.call_args.args[0]
        self.assertEqual(cmd[cmd.index('-crf')+1], '17')
        self.assertEqual(cmd[cmd.index('-c:a')+1], 'copy')
        self.assertIn('+faststart',cmd)
if __name__ == '__main__': unittest.main()
