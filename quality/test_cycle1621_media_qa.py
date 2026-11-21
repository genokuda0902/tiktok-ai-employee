import unittest
from unittest.mock import patch
from quality.cycle1621_media_qa import review

class TestFailClosed(unittest.TestCase):
    @patch("quality.cycle1621_media_qa.probe")
    def test_silent_rejected(self, p):
        p.return_value={"streams":[{"codec_type":"video","width":720,"height":1280}],"format":{"duration":"12"}}
        r=review("demo.mp4")
        self.assertFalse(r["publishable"])
        self.assertIn("missing_audio",r["issues"])
    @patch("quality.cycle1621_media_qa.probe")
    def test_all_gates_explicit(self,p):
        p.return_value={"streams":[{"codec_type":"video","width":1080,"height":1920},{"codec_type":"audio","codec_name":"aac"}],"format":{"duration":"15"}}
        self.assertTrue(review("x",True,True,True)["publishable"])
        self.assertFalse(review("x",True,False,True)["publishable"])
if __name__=="__main__":unittest.main()
