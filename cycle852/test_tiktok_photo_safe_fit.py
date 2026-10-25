"""CI checks for cycle852 reusable photo-fit core."""
import tempfile, unittest
from pathlib import Path
from PIL import Image
from tiktok_photo_safe_fit import MAX_UPSCALE, GENRES, contain_native, validate_inputs, REVIEW_GATE

class TestSafeFit(unittest.TestCase):
    def test_genres(self):
        self.assertEqual(len(GENRES), 10)

    def test_no_crop(self):
        source = Image.new('RGB', (534, 444))
        fitted, scale = contain_native(source, 852, 728)
        self.assertLessEqual(scale, MAX_UPSCALE)
        self.assertEqual(fitted.size, (int(534 * scale), int(444 * scale)))

    def test_no_enlargement_beyond_limit(self):
        for w, h in [(534, 444), (822, 859), (680, 650)]:
            _, scale = contain_native(Image.new('RGB', (w, h)), 852, 728)
            self.assertLessEqual(scale, 1.12)

    def test_validation(self):
        with tempfile.TemporaryDirectory() as tmp:
            files = [Path(tmp) / f'{i}.jpg' for i in range(8)]
            for file in files:
                file.touch()
            beats = [{'start': i * .9, 'end': i * .9 + .8, 'text': '例'} for i in range(24)]
            self.assertTrue(validate_inputs(files, beats, 'ai_work'))
            with self.assertRaises(ValueError):
                validate_inputs(files[:7], beats, 'ai_work')
            with self.assertRaises(ValueError):
                validate_inputs(files, beats[:23], 'ai_work')

    def test_review_gate(self):
        self.assertFalse(any(REVIEW_GATE.values()))

if __name__ == '__main__':
    unittest.main()
