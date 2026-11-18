import unittest
from unittest.mock import patch
from pathlib import Path
from tempfile import TemporaryDirectory
from qa_video import inspect

class QATests(unittest.TestCase):
    def test_missing(self):
        with self.assertRaises(ValueError): inspect("/no/such/video.mp4")
    def test_silent_video_is_not_approved(self):
        with TemporaryDirectory() as d:
            p=Path(d)/"x.mp4"; p.write_bytes(b"fake")
            data={"streams":[{"codec_type":"video","codec_name":"h264","width":720,"height":1280}],"format":{}}
            with patch("qa_video.subprocess.check_output",return_value=__import__("json").dumps(data).encode()),patch("qa_video.subprocess.run"):
                result=inspect(p)
            self.assertFalse(result["audio_present"])
            self.assertFalse(result["publication_approved"])
if __name__=="__main__": unittest.main()
