import unittest
from prompt_typing import (GENRES,PROMPTS,POLICY,START,END,OVERLAY_Y,PATCH_HEIGHT,
    validate_prompt,validate_manifest,visible_lines,char_count,draw_patch,safe_geometry)

class TestPromptTyping(unittest.TestCase):
    def test_all_ten_genres(self):
        self.assertEqual(len(GENRES),10)
        self.assertEqual(set(GENRES),set(PROMPTS))
        for g in GENRES:validate_prompt(PROMPTS[g])
    def test_early_empty(self):self.assertEqual(visible_lines(0,PROMPTS['ai_productivity']),('','',''))
    def test_full_end(self):self.assertEqual(visible_lines(END-START-1,PROMPTS['ai_productivity']),PROMPTS['ai_productivity'])
    def test_monotone(self):
        x=[char_count(i,PROMPTS['ai_productivity']) for i in range(END-START)]
        self.assertEqual(x,sorted(x))
    def test_never_overflow_chars(self):
        for g in GENRES:
            for i in range(END-START):
                v=visible_lines(i,PROMPTS[g])
                self.assertTrue(all(len(a)<=len(b) for a,b in zip(v,PROMPTS[g])))
    def test_safe_region(self):self.assertTrue(safe_geometry());self.assertLess(OVERLAY_Y+PATCH_HEIGHT,1438)
    def test_patch_rgba(self):self.assertEqual(draw_patch(20).mode,'RGBA')
    def test_patch_dimensions(self):self.assertEqual(draw_patch(20).size,(1080,PATCH_HEIGHT))
    def test_patch_transparency(self):self.assertEqual(draw_patch(20).getpixel((5,5))[3],0)
    def test_render_all_genres(self):
        for g in GENRES:self.assertEqual(draw_patch(END-START-1,g).size,(1080,PATCH_HEIGHT))
    def test_reject_external_url(self):
        with self.assertRaises(ValueError):validate_prompt(('https://example.com','ok','ok'))
    def test_reject_phone(self):
        with self.assertRaises(ValueError):validate_prompt(('09012345678','ok','ok'))
    def test_reject_multiline(self):
        with self.assertRaises(ValueError):validate_prompt(('a\nb','ok','ok'))
    def test_reject_unknown_genre(self):
        with self.assertRaises(ValueError):draw_patch(10,'unknown')
    def test_reject_invalid_frame(self):
        with self.assertRaises(ValueError):char_count(END-START,PROMPTS['ai_productivity'])
    def test_policy_never_approved(self):
        self.assertTrue(POLICY['review_only'])
        self.assertFalse(POLICY['publication_approved'])
        self.assertFalse(POLICY['external_upload'])
        self.assertFalse(POLICY['automatic_posting'])
    def test_manifest_hash_fail_closed(self):
        import tempfile,pathlib
        with tempfile.TemporaryDirectory() as d:
            f=pathlib.Path(d)/'src';f.write_bytes(b'video')
            with self.assertRaises(ValueError):
                validate_manifest({**POLICY,'source_sha256':'bad'},f)
    def test_manifest_policy_fail_closed(self):
        import tempfile,pathlib,hashlib
        with tempfile.TemporaryDirectory() as d:
            f=pathlib.Path(d)/'src';f.write_bytes(b'video')
            with self.assertRaises(ValueError):
                validate_manifest({**POLICY,'publication_approved':True,
                    'source_sha256':hashlib.sha256(b'video').hexdigest()},f)

if __name__=='__main__':unittest.main()
