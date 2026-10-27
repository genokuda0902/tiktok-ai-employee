import os, tempfile, unittest
from pathlib import Path
from offline_save_proof import GENRES,STORIES,Story,validate_story,stage,html_document,validate_manifest,sha256,POLICY,draw_frame

class Cycle886Tests(unittest.TestCase):
    def test_genres(self):
        self.assertEqual(len(GENRES),10)
        for s in STORIES.values():self.assertTrue(validate_story(s))
    def test_reject_unknown_genre(self):
        with self.assertRaises(ValueError):validate_story(Story("unknown","x","y","z"))
    def test_reject_unsafe_url(self):
        with self.assertRaises(ValueError):validate_story(Story("career","https://example.com","x","z"))
    def test_reject_phone(self):
        with self.assertRaises(ValueError):validate_story(Story("career","090-1234-5678","x","z"))
    def test_reject_empty(self):
        with self.assertRaises(ValueError):validate_story(Story("career","","x","z"))
    def test_three_stages(self):
        self.assertEqual([stage(x) for x in (0,25,26,51,52,77)],[0,0,1,1,2,2])
    def test_out_of_range(self):
        with self.assertRaises(ValueError):stage(78)
    def test_html_offline(self):
        s=html_document()
        self.assertNotIn("http://",s);self.assertNotIn("https://",s)
        self.assertIn("reduce(",s);self.assertIn("window.savedTemplate",s)
    def test_source_hash_gate(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)/"s";p.write_bytes(b"test")
            m=dict(POLICY,source_sha256="wrong")
            with self.assertRaises(ValueError):validate_manifest(m,p)
    def test_publication_gate(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)/"s";p.write_bytes(b"test")
            m=dict(POLICY,source_sha256=sha256(p));m["publication_approved"]=True
            with self.assertRaises(ValueError):validate_manifest(m,p)
    @unittest.skipUnless(os.environ.get("CYCLE886_BROWSER_QA")=="1","Chromium-only local test")
    def test_real_browser_dom(self):
        from offline_save_proof import capture_browser
        with tempfile.TemporaryDirectory() as d:
            self.assertEqual(len(set(capture_browser(d))),3)
    @unittest.skipUnless(os.environ.get("CYCLE886_BROWSER_QA")=="1","Chromium-only local test")
    def test_caption_safe_overlay(self):
        from offline_save_proof import capture_browser
        from PIL import Image
        with tempfile.TemporaryDirectory() as d:
            capture_browser(d)
            imgs=[Image.open(Path(d)/x) for x in ("01_input.png","02_verified.png","03_saved.png")]
            for f in (0,26,52,77):
                a=draw_frame(f,imgs)
                self.assertEqual(a.size,(1080,1438))
                self.assertEqual(a.getpixel((0,0))[3],0)
                self.assertGreater(a.getpixel((500,800))[3],0)

if __name__=="__main__":unittest.main()
