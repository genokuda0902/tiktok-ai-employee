import unittest
try:
    from .contract import PALETTES, SCENE3_BOX, validate_graphic_box, validate_timeline, require_human_review, proof_command_output
except ImportError:
    from contract import PALETTES, SCENE3_BOX, validate_graphic_box, validate_timeline, require_human_review, proof_command_output

class TestCycle681Contract(unittest.TestCase):
    def test_ten_genres(self):
        self.assertEqual(len(PALETTES),10)
    def test_safe_zone(self):
        self.assertTrue(validate_graphic_box(SCENE3_BOX))
        with self.assertRaises(ValueError): validate_graphic_box((0,1400,100,200))
    def test_approval_gate(self):
        self.assertIn("NOT_APPROVED",require_human_review())
        with self.assertRaises(ValueError): require_human_review(auto_post=True)
        with self.assertRaises(ValueError): require_human_review(approved=True)
    def test_proof(self):
        self.assertEqual(proof_command_output(),"Hello!")
    def test_timeline(self):
        self.assertEqual(validate_timeline([
            {"scene":1,"start":0,"end":1,"spoken_text":"こんにちは","caption_kind":"editorial_not_transcript"},
            {"scene":2,"start":1,"end":2,"spoken_text":"","caption_kind":"silent_end_card"}
        ]),2.)
if __name__=="__main__": unittest.main()
