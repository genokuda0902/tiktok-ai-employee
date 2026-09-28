import unittest
from video_engine.slide_first_storyboard import BEATS, SlideCard, validate_slide_first


def cards():
    return [SlideCard(b, f"{b}.png", b, f"voice-{b}", f"caption-{b}", True, True) for b in BEATS]

class SlideFirstStoryboardTest(unittest.TestCase):
    def test_valid_six_beat_story(self):
        validate_slide_first(cards())

    def test_wrong_order_fails(self):
        x = cards(); x[0], x[1] = x[1], x[0]
        with self.assertRaises(ValueError): validate_slide_first(x)

    def test_duplicate_image_fails(self):
        x = cards(); x[1] = SlideCard(x[1].beat, x[0].image_path, x[1].headline, x[1].narration, x[1].caption, True, True)
        with self.assertRaises(ValueError): validate_slide_first(x)

    def test_unapproved_fails_closed(self):
        x = cards(); c=x[2]; x[2]=SlideCard(c.beat,c.image_path,c.headline,c.narration,c.caption,False,True)
        with self.assertRaises(ValueError): validate_slide_first(x)

    def test_wrong_resolution_fails(self):
        with self.assertRaises(ValueError): validate_slide_first(cards(),720,1280)

if __name__ == "__main__": unittest.main()
