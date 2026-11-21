import unittest


def release_allowed(video_ok, japanese_audio_verified, captions_synced, rights_cleared, employee_approved):
    return all((video_ok, japanese_audio_verified, captions_synced, rights_cleared, employee_approved))


class QualityGateTests(unittest.TestCase):
    def test_unverified_narration_blocks_release(self):
        self.assertFalse(release_allowed(True, False, True, True, True))

    def test_unsynced_captions_block_release(self):
        self.assertFalse(release_allowed(True, True, False, True, True))

    def test_approval_required(self):
        self.assertFalse(release_allowed(True, True, True, True, False))

    def test_all_checks_required(self):
        self.assertTrue(release_allowed(True, True, True, True, True))


if __name__ == '__main__':
    unittest.main()
