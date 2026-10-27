import unittest
from dataclasses import replace
from browser_proof_core import *
class BrowserProofTests(unittest.TestCase):
    def test_ten_genres(self):
        for g in GENRES:
            with self.subTest(g=g):self.assertTrue(validate(g))
    def test_exact_duration(self):self.assertEqual(sum(c.end-c.start for c in timeline()),691)
    def test_unique_22_states(self):self.assertEqual(len(timeline()),22)
    def test_13_real_browser_states(self):self.assertEqual(sum(c.scene in STAGES for c in timeline()),13)
    def test_no_gap(self):
        a=list(timeline());a[3]=replace(a[3],start=a[3].start+1)
        with self.assertRaises(ValueError):validate(clips=a)
    def test_no_overlap(self):
        a=list(timeline());a[3]=replace(a[3],start=a[3].start-1)
        with self.assertRaises(ValueError):validate(clips=a)
    def test_safe_caption_box(self):self.assertTrue(validate(box=(110,520,970,1210)))
    def test_reject_caption_overlap(self):
        with self.assertRaises(ValueError):validate(box=(110,520,970,1510))
    def test_reject_external_url(self):
        with self.assertRaises(ValueError):safe_browser_source('https://example.com')
    def test_reject_external_requests(self):
        with self.assertRaises(ValueError):safe_browser_source('about:blank / page.set_content(local HTML)',1)
    def test_reject_private_data(self):
        with self.assertRaises(ValueError):safe_browser_source('about:blank / page.set_content(local HTML)',0,True)
    def test_allow_local(self):self.assertTrue(safe_browser_source('about:blank / page.set_content(local HTML)'))
    def test_unknown_genre(self):
        with self.assertRaises(ValueError):validate('wrong')
if __name__=='__main__':unittest.main()
