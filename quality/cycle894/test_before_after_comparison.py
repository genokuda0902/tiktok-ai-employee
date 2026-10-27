import unittest
from before_after_comparison import GENRES, POLICY, X, Y, W, H, draw_patch, stage, validate_copy

BASE={'genre':'ai_productivity',**POLICY,'before_title':'手作業','after_title':'テンプレ活用',
      'before_steps':['転記','集計','確認'],'after_steps':['指示','整理','元データ照合'],'cta':'保存して試す'}

class BeforeAfterTests(unittest.TestCase):
    def test_all_ten_genres(self):
        for g in GENRES:
            self.assertTrue(validate_copy({**BASE,'genre':g}))
    def test_unknown_genre(self):
        with self.assertRaises(ValueError):validate_copy({**BASE,'genre':'unknown'})
    def test_fail_closed_release(self):
        for k in POLICY:
            with self.subTest(k=k),self.assertRaises(ValueError):validate_copy({**BASE,k:not POLICY[k]})
    def test_pii_block(self):
        for s in ('a@example.com','https://x.com','09012345678'):
            with self.subTest(s=s),self.assertRaises(ValueError):validate_copy({**BASE,'cta':s})
    def test_unverified_speed_claim_block(self):
        for s in ('10分短縮','50%改善','2倍アップ'):
            with self.subTest(s=s),self.assertRaises(ValueError):validate_copy({**BASE,'cta':s})
    def test_three_steps_required(self):
        with self.assertRaises(ValueError):validate_copy({**BASE,'after_steps':['一つ']})
    def test_difference_required(self):
        with self.assertRaises(ValueError):validate_copy({**BASE,'after_steps':BASE['before_steps']})
    def test_stages(self):
        self.assertEqual([stage(f) for f in (0,34,35,69,70,102)],[0,0,1,1,2,2])
    def test_out_of_range(self):
        for f in (-1,103,1.2):
            with self.assertRaises(ValueError):stage(f)
    def test_safe_geometry(self):
        self.assertTrue(Y>=160 and Y+H<1480 and X>=60 and X+W<=1020)
    def test_rendered_stages_differ(self):
        im=[draw_patch(f,BASE) for f in (8,46,86)]
        self.assertEqual(im[0].size,(W,H))
        self.assertNotEqual(im[0].tobytes(),im[1].tobytes())
        self.assertNotEqual(im[1].tobytes(),im[2].tobytes())
    def test_missing_fields(self):
        with self.assertRaises(ValueError):validate_copy({'genre':'ai_productivity'})

if __name__=='__main__':unittest.main()
