import unittest
from video_engine.unified_story_manifest import StoryCut, StoryManifest
from video_engine.semantic_uniqueness_guard import validate_semantic_uniqueness, release_contract

def manifest(repeat=False):
    cuts=[]
    for i in range(10):
        j=0 if repeat else i
        narration=f"手順{j}を確認すると作業時間を短縮できます"
        cuts.append(StoryCut(f"approved scene {j}", f"手順{j}", narration, f"手順{j}", 3.0))
    return StoryManifest("common", cuts)

class SemanticUniquenessGuardTests(unittest.TestCase):
    def test_ten_distinct_beats_pass(self):
        r=validate_semantic_uniqueness(manifest())
        self.assertEqual(r["image_copy"]["unique"],10)
    def test_looped_story_fails_closed(self):
        with self.assertRaisesRegex(ValueError,"repeats too much"):
            validate_semantic_uniqueness(manifest(True))
    def test_unsafe_threshold_rejected(self):
        with self.assertRaises(ValueError):
            validate_semantic_uniqueness(manifest(),0.5)
    def test_release_stays_manual(self):
        c=release_contract()
        self.assertTrue(c["zero_cost"])
        self.assertTrue(c["reject_looped_story"])
        self.assertTrue(c["human_approval_required"])
        self.assertTrue(c["manual_post_only"])
        self.assertFalse(c["auto_post"])

if __name__=="__main__":
    unittest.main()
