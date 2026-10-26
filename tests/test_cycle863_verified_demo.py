import unittest
from tools.cycle863_verified_demo import (
    GENRE_ACCENTS,SAMPLE_TASKS,compute_progress,generate_email,
    revise_conclusion_first,scene_at,demo_payload)

class VerifiedCalculationTests(unittest.TestCase):
    def test_default_math(self):
        self.assertEqual(compute_progress(),{"total":4,"done":3,"pending":1,"percent":75})
    def test_zero(self):
        self.assertEqual(compute_progress((("a",False),))["percent"],0)
    def test_full(self):
        self.assertEqual(compute_progress((("a",True),))["percent"],100)
    def test_empty(self):
        with self.assertRaises(ValueError): compute_progress(())
    def test_invalid_flag(self):
        with self.assertRaises(TypeError): compute_progress((("a",1),))
    def test_length(self):
        self.assertLessEqual(len(generate_email(compute_progress())),150)
    def test_too_long(self):
        with self.assertRaises(ValueError): generate_email(compute_progress(),3)
    def test_real_revision(self):
        before=generate_email(compute_progress())
        after=revise_conclusion_first(before)
        self.assertNotEqual(before,after)
        self.assertTrue(after.startswith("今週の進捗"))
        self.assertEqual(sorted(before.split("。")),sorted(after.split("。")))
    def test_ten_genres(self):
        self.assertEqual(len(GENRE_ACCENTS),10)
        self.assertEqual(len(set(GENRE_ACCENTS.values())),10)
    def test_scene_boundaries(self):
        self.assertEqual(scene_at(0),0)
        self.assertEqual(scene_at(9.8),3)
        self.assertEqual(scene_at(23.0),7)
    def test_payload(self):
        p=demo_payload()
        self.assertTrue(p["synthetic"])
        self.assertTrue(p["within_150_chars"])
        self.assertEqual(p["stats"]["percent"],75)
    def test_no_personal_data(self):
        text=generate_email(compute_progress())
        self.assertNotIn("@",text)
        self.assertNotIn("電話",text)

if __name__=="__main__":unittest.main()
