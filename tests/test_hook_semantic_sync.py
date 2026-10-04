import unittest

from video_engine.quality.hook_semantic_sync import validate_hook_semantic_sync


def valid_hook():
    return {
        "start_seconds": 0.0,
        "end_seconds": 1.5,
        "claim_id": "organize-three-fields",
        "visual_claim_id": "organize-three-fields",
        "audio_claim_id": "organize-three-fields",
        "caption_claim_id": "organize-three-fields",
        "caption_text": "AIで3項目に整理",
        "narration_text": "AIで分類、要点、次のアクションに整理します。",
        "auto_post": False,
        "publication": "HUMAN_REVIEW",
    }


class HookSemanticSyncTests(unittest.TestCase):
    def test_valid_hook_passes(self):
        ok, errors = validate_hook_semantic_sync(valid_hook())
        self.assertTrue(ok)
        self.assertEqual([], errors)

    def test_audio_claim_mismatch_fails_closed(self):
        hook = valid_hook()
        hook["audio_claim_id"] = "different-claim"
        ok, errors = validate_hook_semantic_sync(hook)
        self.assertFalse(ok)
        self.assertIn("audio_claim_id_mismatch", errors)

    def test_missing_narration_fails_closed(self):
        hook = valid_hook()
        hook["narration_text"] = ""
        ok, errors = validate_hook_semantic_sync(hook)
        self.assertFalse(ok)
        self.assertIn("hook_narration_missing", errors)

    def test_auto_post_is_forbidden(self):
        hook = valid_hook()
        hook["auto_post"] = True
        ok, errors = validate_hook_semantic_sync(hook)
        self.assertFalse(ok)
        self.assertIn("auto_post_forbidden", errors)

    def test_hook_after_first_1_5_seconds_fails(self):
        hook = valid_hook()
        hook["end_seconds"] = 1.51
        ok, errors = validate_hook_semantic_sync(hook)
        self.assertFalse(ok)
        self.assertIn("hook_outside_first_1_5s", errors)


if __name__ == "__main__":
    unittest.main()
