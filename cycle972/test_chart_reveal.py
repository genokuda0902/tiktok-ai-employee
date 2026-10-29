import unittest
from chart_reveal import artwork, visible_height, DATA, TOTALS, require_genre, ART_BOTTOM, MONTHS

class ChartRevealTests(unittest.TestCase):
    def test_arithmetic(self):
        self.assertEqual(TOTALS,{'営業A':46,'営業B':29})
        self.assertEqual(sum(DATA['営業A']),46)
        self.assertEqual(sum(DATA['営業B']),29)
    def test_three_months(self):
        self.assertEqual(MONTHS,('4月','5月','6月'))
        self.assertEqual(len(DATA['営業A']),3)
    def test_progression(self):
        for i in range(3):
            self.assertEqual(visible_height(0,i),0)
            self.assertAlmostEqual(visible_height(1,i),1)
        self.assertGreater(visible_height(.3,0),visible_height(.3,1))
        self.assertGreater(visible_height(.52,1),visible_height(.52,2))
    def test_geometry(self):
        self.assertEqual(artwork(0).size,(1080,ART_BOTTOM))
        self.assertEqual(ART_BOTTOM,1240)
    def test_animation_changes_pixels(self):
        self.assertNotEqual(artwork(.15).tobytes(),artwork(.87).tobytes())
    def test_fail_closed_unknown(self):
        with self.assertRaises(ValueError):require_genre('unknown')
    def test_fail_closed_nine_unreviewed(self):
        for g in ('business','finance','health','beauty','travel','education','food','life_hacks','tech'):
            with self.assertRaises(PermissionError):artwork(.5,g)
    def test_review_only(self):
        require_genre('ai_work')
    def test_early_vs_late(self):
        self.assertNotEqual(artwork(0).tobytes(),artwork(1).tobytes())

if __name__=='__main__':unittest.main()
