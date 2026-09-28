import unittest
from storyboard_panel_renderer import DEFAULT_PANELS, Panel, crop_box, validate_panels

class StoryboardPanelRendererTests(unittest.TestCase):
    def test_default_valid(self):
        self.assertTrue(validate_panels(DEFAULT_PANELS))

    def test_default_uses_six_unique_panels(self):
        self.assertEqual(len({p.index for p in DEFAULT_PANELS}), 6)

    def test_crop_box(self):
        self.assertEqual(crop_box(900, 1600, 5), (300, 400, 600, 800))

    def test_duplicate_fails_closed(self):
        with self.assertRaises(ValueError):
            validate_panels((Panel(1, 'a', 1), Panel(1, 'b', 1)))

    def test_blank_caption_fails_closed(self):
        with self.assertRaises(ValueError):
            validate_panels((Panel(1, ' ', 1),))

if __name__ == '__main__':
    unittest.main()
