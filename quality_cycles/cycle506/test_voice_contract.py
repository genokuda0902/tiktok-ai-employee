import unittest
from voice_contract import check, GENRES
class ContractTest(unittest.TestCase):
    def test_genres(self): self.assertEqual(len(set(GENRES)),10)
    def test_unapproved(self): self.assertFalse(check({"resolution":[1080,1920],"full_decode":"PASS"})["publishable"])
    def test_phonetic_rejected(self): self.assertFalse(check({"native_japanese_voice":"NOT_NATIVE_ROMAJI_PREVIEW"})["publishable"])
    def test_positive(self):
        q={"native_japanese_voice":"HUMAN_VERIFIED","voice_caption_sync":"PASS","human_review":"APPROVED","publication":"MANUAL_POST_APPROVED","full_decode":"PASS","resolution":[1080,1920],"personal_data":"NONE","rights":"ORIGINAL_AND_CLEARED"}
        self.assertTrue(check(q)["publishable"])
if __name__=="__main__":unittest.main()
