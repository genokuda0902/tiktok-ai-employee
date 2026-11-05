import unittest
from qa_review_video import check_review_media

def sample():
    return {"streams":[{"codec_type":"video","codec_name":"h264","width":1080,"height":1920}],"format":{"duration":"15.0"}}

class TestReviewQA(unittest.TestCase):
    def test_review_is_never_publication_approved(self):
        self.assertFalse(check_review_media(sample())["publication_approved"])
    def test_silent_is_reported(self):
        self.assertFalse(check_review_media(sample())["has_audio"])
    def test_reject_wrong_resolution(self):
        item=sample();item["streams"][0]["width"]=720
        with self.assertRaises(ValueError):check_review_media(item)
if __name__=="__main__": unittest.main()
