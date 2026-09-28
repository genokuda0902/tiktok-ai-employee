import unittest
from video_engine.narration_sync_guard import CutTiming, validate_narration_sync

def valid_cuts():
    return tuple(CutTiming(f"場面{i}の説明です", f"場面{i}", 3.0, 3.0) for i in range(10))

class NarrationSyncGuardTests(unittest.TestCase):
    def test_valid_ten_cut_story_passes(self):
        result=validate_narration_sync(valid_cuts())
        self.assertEqual(result["cuts"],10)
        self.assertEqual(result["unique_ratio"],1.0)
        self.assertTrue(result["manual_post_only"])
        self.assertFalse(result["auto_post"])

    def test_reused_narration_fails_closed(self):
        cuts=list(valid_cuts())
        cuts[1]=CutTiming(cuts[0].narration,cuts[0].caption,3.0,3.0)
        with self.assertRaisesRegex(ValueError,"reuse"):
            validate_narration_sync(cuts)

    def test_caption_drift_fails_closed(self):
        cuts=list(valid_cuts())
        cuts[3]=CutTiming("別の説明です","一致しない字幕",3.0,3.0)
        with self.assertRaisesRegex(ValueError,"caption drifts"):
            validate_narration_sync(cuts)

    def test_audio_timeline_drift_fails_closed(self):
        cuts=list(valid_cuts())
        cuts[5]=CutTiming(cuts[5].narration,cuts[5].caption,3.0,3.4)
        with self.assertRaisesRegex(ValueError,"drift"):
            validate_narration_sync(cuts)

if __name__=="__main__":
    unittest.main()
