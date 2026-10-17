import unittest
from safe_layout import TextRegion, PRIMARY_TITLE, FORMULA_UI, FOCUS_STRIP, validate_layout, cue_file
SCENES=((0,60,'その集計、まだ手作業？','hook'),(60,120,'毎回、数字を足していない？','problem'),(120,210,'AIに計算式を聞く','prompt'),(210,300,'B2:B5だけを選択','select'),(300,390,'提案された式を入力','formula'),(390,480,'4つの値で検算','proof'),(480,540,'操作がシンプルに','compare'),(540,600,'保存して次回試そう','cta'))
class TestSafeLayout(unittest.TestCase):
    def test_safe(self):self.assertTrue(validate_layout())
    def test_legacy_bottom_unsafe(self):self.assertFalse(TextRegion('old',35,837,505,865).safe())
    def test_nonoverlap(self):self.assertFalse(FORMULA_UI.overlaps(FOCUS_STRIP))
    def test_eight_cues(self):
        s=cue_file(SCENES)
        self.assertEqual(s.count('-->'),8)
        self.assertIn('00:00:18,000 --> 00:00:20,000',s)
    def test_bad_cue(self):
        with self.assertRaises(ValueError):cue_file([(1,1,'bad','hook')])
if __name__=='__main__':unittest.main()
