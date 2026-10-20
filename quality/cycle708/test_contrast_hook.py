"""Cross-genre unit tests for the rights-safe contrast hook."""
import unittest
from contrast_hook import HookCopy, validate_hook, ease

class ContrastHookTests(unittest.TestCase):
    def test_all_ten_genres(self):
        for n in range(1, 11):
            self.assertTrue(validate_hook(HookCopy(footnote=f'genre_{n:02d} / 説明用')))
    def test_no_unverified_claims(self):
        for c in (HookCopy(after='90%削減'), HookCopy(before='100%改善'),
                  HookCopy(footnote='必ず速くなる')):
            with self.assertRaises(ValueError): validate_hook(c)
    def test_long_labels_rejected(self):
        with self.assertRaises(ValueError):
            validate_hook(HookCopy(before='長いタイトルを入れすぎないようにする'))
    def test_ease_is_clamped(self):
        self.assertEqual(ease(-5), 0)
        self.assertEqual(ease(5), 1)
        self.assertAlmostEqual(ease(.5), .5)

if __name__ == '__main__':
    unittest.main()
