"""Review-only acceptance checks shared across ten genres."""
import unittest


def publication_allowed(metadata):
    required = ('japanese_voice_verified', 'speech_captions_verified',
                'asset_rights_approved', 'privacy_review_passed',
                'employee_approved', 'manual_post_only')
    return all(metadata.get(key) is True for key in required)


class ReviewGateTests(unittest.TestCase):
    def test_silent_video_is_not_approved(self):
        self.assertFalse(publication_allowed({'manual_post_only': True}))

    def test_missing_rights_fails_closed(self):
        data = dict.fromkeys(('japanese_voice_verified', 'speech_captions_verified',
            'asset_rights_approved', 'privacy_review_passed',
            'employee_approved', 'manual_post_only'), True)
        data['asset_rights_approved'] = False
        self.assertFalse(publication_allowed(data))

    def test_all_review_gates_required(self):
        data = dict.fromkeys(('japanese_voice_verified', 'speech_captions_verified',
            'asset_rights_approved', 'privacy_review_passed',
            'employee_approved', 'manual_post_only'), True)
        self.assertTrue(publication_allowed(data))

if __name__ == '__main__':
    unittest.main()
