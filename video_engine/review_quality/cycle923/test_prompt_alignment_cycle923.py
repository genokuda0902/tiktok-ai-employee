import unittest
from prompt_alignment_cycle923 import (
    START,END,FRAME_COUNT,GENRES,EXAMPLES,beat,prompt_text,validate,STATUS
)
class TestPromptAlignment(unittest.TestCase):
    def test_exact_10_genres(self): self.assertEqual(len(GENRES),10)
    def test_all_have_distinct_examples(self):
        self.assertEqual(len({prompt_text(g) for g in GENRES}),10)
    def test_three_fields_each(self):
        for g in GENRES:
            with self.subTest(genre=g):
                self.assertEqual(len(EXAMPLES[g]),3)
                self.assertTrue(all(isinstance(s,str) and 3<=len(s)<=28 for s in EXAMPLES[g]))
    def test_no_private_names(self):
        for x in EXAMPLES.values():
            self.assertFalse(any('奥田' in s or 'ミカ' in s for s in x))
    def test_first_beat(self): self.assertEqual(beat(START),0)
    def test_second_beat(self): self.assertEqual(beat(START+29),1)
    def test_third_beat(self): self.assertEqual(beat(START+58),2)
    def test_last_frame(self): self.assertEqual(beat(END-1),2)
    def test_beat_rejects_outside(self):
        for x in (START-1,END):
            with self.assertRaises(ValueError): beat(x)
    def test_valid(self): validate('ai_work','x_REVIEW_ONLY.mp4')
    def test_reject_bad_genre(self):
        with self.assertRaises(ValueError):validate('crypto','x_REVIEW_ONLY.mp4')
    def test_reject_public_filename(self):
        with self.assertRaises(ValueError):validate('ai_work','x.mp4')
    def test_reject_bad_framecount(self):
        with self.assertRaises(ValueError):validate('ai_work','x_REVIEW_ONLY.mp4',100)
    def test_fail_closed_status(self): self.assertIn('PUBLICATION_NOT_APPROVED',STATUS)
    def test_exact_scene_length(self): self.assertEqual(END-START,87)
if __name__=='__main__': unittest.main()
