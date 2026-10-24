"""Fail-closed tests for opaque, readable action cards across ten genres."""
import unittest
from action_panel import GENRES, LABELS, SCENE, PW, PH, panel_frame, validate, AUTO_POST, EMPLOYEE_APPROVAL

class ActionPanelTests(unittest.TestCase):
    def test_ten_genres(self):
        self.assertEqual(len(GENRES),10)
        for genre in GENRES:
            self.assertEqual(len(validate(genre)),3)
    def test_card_opaque(self):
        for t in (0,28,29,56,57,93):
            im=panel_frame(t)
            self.assertEqual(im.mode,'RGB')
            self.assertEqual(im.size,(PW,PH))
    def test_no_old_text_can_show_through(self):
        im=panel_frame(44)
        self.assertEqual(im.getpixel((410,250))[0] > 0,True)
        self.assertNotEqual(im.mode,'RGBA')
    def test_reject_invalid(self):
        with self.assertRaises(ValueError): panel_frame(-1)
        with self.assertRaises(ValueError): panel_frame(SCENE)
        with self.assertRaises(ValueError): validate('unapproved_genre')
    def test_safe_labels(self):
        self.assertEqual(LABELS,('誰が','何を','いつまで'))
    def test_no_publication(self):
        self.assertFalse(AUTO_POST)
        self.assertFalse(EMPLOYEE_APPROVAL)

if __name__=='__main__': unittest.main()
