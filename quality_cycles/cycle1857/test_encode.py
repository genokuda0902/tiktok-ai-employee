import unittest
from pathlib import Path
from unittest.mock import patch
from encode import encode
class TestEncode(unittest.TestCase):
    def test_crf_guard(self):
        with self.assertRaises(ValueError): encode(Path("in"),Path("out"),-1)
    def test_audio_copy_and_faststart(self):
        with patch("subprocess.run") as run:
            encode(Path("in"),Path("out"))
            args=run.call_args.args[0]
            self.assertIn("+faststart",args)
            self.assertEqual(args[args.index("-c:a")+1],"copy")
if __name__=="__main__": unittest.main()
