import unittest

from video_engine.viewer_copy_guard import (
    leaked_role_labels,
    release_contract,
    validate_viewer_copy,
)


class ViewerCopyGuardTests(unittest.TestCase):
    def test_numbered_internal_role_labels_fail_closed(self):
        samples = ["01 HOOK", "02 PROBLEM", "03 DEMO", "10 CTA"]
        with self.assertRaisesRegex(ValueError, "internal role labels leaked"):
            validate_viewer_copy(samples)

    def test_plain_internal_role_labels_fail_closed(self):
        self.assertEqual(leaked_role_labels(["HOOK", "AFTER", "CTA"]), ["HOOK", "AFTER", "CTA"])

    def test_real_viewer_copy_is_allowed(self):
        self.assertTrue(validate_viewer_copy([
            "毎日のExcel集計、まだ手作業？",
            "まず「繰り返し」を見つける",
            "10分の作業を1分へ",
        ]))

    def test_release_policy_remains_manual_and_zero_cost(self):
        policy = release_contract()
        self.assertTrue(policy["zero_cost"])
        self.assertTrue(policy["human_approval_required"])
        self.assertTrue(policy["manual_post_only"])
        self.assertFalse(policy["auto_post"])


if __name__ == "__main__":
    unittest.main()
