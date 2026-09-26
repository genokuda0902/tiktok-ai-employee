import tempfile
import unittest
from pathlib import Path
from PIL import Image
from video_engine.production_v2.assets import register
class AssetTests(unittest.TestCase):
    def test_ai_image_provenance_and_native_dimensions(self):
        with tempfile.TemporaryDirectory() as d:
            file=Path(d)/'image.png';Image.new('RGB',(1080,1920)).save(file)
            with self.assertRaises(ValueError):register(file,'a','ai_image','ChatGPT','user-created','generation record')
            item=register(file,'a','ai_image','ChatGPT','user-created','generation record',visual_prompt='original illustration',model='image model',generated_at='2026-09-27T00:00:00Z')
            self.assertTrue(item['ai_disclosure']);self.assertFalse(item['publication_approved'])
            self.assertEqual(len(item['sha256']),64)
if __name__=='__main__':unittest.main()
