import unittest
from proof_contract import validate


def plan():
    ends = [1.5, 4, 6.5, 9, 11.5, 14, 17, 20]
    starts = [0] + ends[:-1]
    return [dict(start=a, end=b, caption='確認', keyframes=2) for a, b in zip(starts, ends)]


class ProofTests(unittest.TestCase):
    def test_valid(self):
        self.assertTrue(validate(plan()))

    def test_gap(self):
        scenes = plan(); scenes[3]['start'] += .1
        with self.assertRaises(ValueError): validate(scenes)

    def test_hook_late(self):
        scenes = plan(); scenes[0]['end'] = 2; scenes[1]['start'] = 2
        with self.assertRaises(ValueError): validate(scenes)

    def test_few_keyframes(self):
        scenes = plan(); scenes[4]['keyframes'] = 1
        with self.assertRaises(ValueError): validate(scenes)

    def test_caption_overflow(self):
        scenes = plan(); scenes[1]['caption'] = 'あ' * 29
        with self.assertRaises(ValueError): validate(scenes)


if __name__ == '__main__': unittest.main()
