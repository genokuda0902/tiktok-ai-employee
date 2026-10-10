import unittest

from quality.cycle484.formula_proof import ProofBeat, validate_proof_beat


def example(**kwargs):
    fields = dict(start=10.0, end=12.0, label="SUM(B2:B5) = 720",
                  source_kind="SYNTHETIC_DEMO", source_values=(120,150,200,250),
                  claimed_total=720, safe_bbox=(90,620,990,1390))
    fields.update(kwargs)
    return ProofBeat(**fields)


class FormulaProofTests(unittest.TestCase):
    def check(self, beat=None, **kwargs):
        return validate_proof_beat(beat or example(), video_duration=20.15,
                                   source_rights="SYNTHETIC_LOCAL", **kwargs)

    def test_valid(self):
        self.assertEqual(self.check()["total"], 720)

    def test_false_total_fails(self):
        with self.assertRaises(ValueError): self.check(example(claimed_total=721))

    def test_missing_source_fails(self):
        with self.assertRaises(ValueError): self.check(example(source_values=()))

    def test_wrong_source_label_fails(self):
        with self.assertRaises(ValueError): self.check(example(source_kind="REAL_USER_EXCEL"))

    def test_outside_video_fails(self):
        with self.assertRaises(ValueError): self.check(example(end=30.0))

    def test_caption_collision_fails(self):
        with self.assertRaises(ValueError): self.check(example(safe_bbox=(0,10,1080,1900)))

    def test_auto_post_fails(self):
        with self.assertRaises(ValueError): self.check(auto_post=True)

    def test_publication_fails(self):
        with self.assertRaises(ValueError): self.check(publication="APPROVED")

    def test_negative_source_fails(self):
        with self.assertRaises(ValueError): self.check(example(source_values=(-1,150,200,250)))

    def test_unallowlisted_rights_fails(self):
        with self.assertRaises(ValueError):
            validate_proof_beat(example(),video_duration=20.15,source_rights="UNKNOWN")


if __name__ == "__main__":
    unittest.main()
