import unittest
from video_engine.hook_banner import HookBanner, require_human_approval

class HookBannerTests(unittest.TestCase):
    def test_valid_vertical_canvas(self):
        HookBanner().validate(1080, 1920)

    def test_rejects_wrong_canvas(self):
        with self.assertRaises(ValueError):
            HookBanner().validate(720, 1280)

    def test_rejects_banner_after_first_three_seconds(self):
        with self.assertRaises(ValueError):
            HookBanner(start=2.5, end=3.2).validate(1080, 1920)

    def test_human_approval_is_fail_closed(self):
        with self.assertRaises(PermissionError):
            require_human_approval(False)

if __name__ == '__main__':
    unittest.main()
