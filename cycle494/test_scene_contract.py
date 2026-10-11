import unittest
from scene_contract import GENRES, SIZE, FPS, SCENE_SECONDS, BEATS, SCENE_KEYS, is_ready
class SceneContractTests(unittest.TestCase):
    def test_genres(self): self.assertEqual(len(GENRES),10)
    def test_size(self): self.assertEqual(SIZE,(1080,1920))
    def test_fps(self): self.assertEqual(FPS,30)
    def test_scene_count(self): self.assertEqual(len(SCENE_KEYS),6)
    def test_beats(self): self.assertEqual(BEATS,12)
    def test_length(self): self.assertAlmostEqual(len(SCENE_KEYS)*SCENE_SECONDS,19.2)
    def test_missing_native_voice_blocks(self): self.assertFalse(is_ready({"decode_ok":True,"human_approved":True,"rights_ok":True}))
    def test_human_approval_required(self): self.assertFalse(is_ready({"native_ja_voice_reviewed":True,"decode_ok":True,"rights_ok":True}))
    def test_explicit_approval_only(self): self.assertTrue(is_ready({"native_ja_voice_reviewed":True,"decode_ok":True,"human_approved":True,"rights_ok":True}))
if __name__=="__main__": unittest.main()
