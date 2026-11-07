import unittest
from quality.cycle1289_media_contract import MediaQA, publication_ready, review_label

class TestMediaQA(unittest.TestCase):
    def test_silent_1080p_is_not_publishable(self):
        q=MediaQA(1080,1920,12,False,False,True,True)
        self.assertFalse(publication_ready(q))
        self.assertEqual(review_label(q),'REVIEW_ONLY_NOT_APPROVED')
    def test_requires_every_approval(self):
        q=MediaQA(1080,1920,12,True,True,True,False)
        self.assertFalse(publication_ready(q))
    def test_approved_media(self):
        self.assertTrue(publication_ready(MediaQA(1080,1920,12,True,True,True,True)))
if __name__=='__main__': unittest.main()
