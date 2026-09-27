import tempfile
import unittest
from pathlib import Path
from PIL import Image
from video_engine.production_v2.assets import register, validate_for_render

class AssetTests(unittest.TestCase):
    def _registered_image(self, folder):
        file=Path(folder)/'image.png'
        Image.new('RGB',(1080,1920)).save(file)
        return file, register(
            file,'a','ai_image','ChatGPT','user-created','generation record',
            visual_prompt='original illustration',model='image model',
            generated_at='2026-09-27T00:00:00Z'
        )

    def test_ai_image_provenance_and_native_dimensions(self):
        with tempfile.TemporaryDirectory() as d:
            file=Path(d)/'image.png';Image.new('RGB',(1080,1920)).save(file)
            with self.assertRaises(ValueError):
                register(file,'a','ai_image','ChatGPT','user-created','generation record')
            item=register(
                file,'a','ai_image','ChatGPT','user-created','generation record',
                visual_prompt='original illustration',model='image model',
                generated_at='2026-09-27T00:00:00Z'
            )
            self.assertTrue(item['ai_disclosure'])
            self.assertFalse(item['publication_approved'])
            self.assertEqual(len(item['sha256']),64)

    def test_render_gate_fails_closed_and_detects_post_approval_mutation(self):
        with tempfile.TemporaryDirectory() as d:
            file,item=self._registered_image(d)
            with self.assertRaisesRegex(ValueError,'Privacy review'):
                validate_for_render(item)
            item['privacy_review']='approved'
            with self.assertRaisesRegex(ValueError,'Publication approval'):
                validate_for_render(item)
            item['publication_approved']=True
            self.assertIs(validate_for_render(item),item)
            Image.new('RGB',(1080,1920),(1,2,3)).save(file)
            with self.assertRaisesRegex(ValueError,'checksum changed'):
                validate_for_render(item)

    def test_render_gate_requires_rights_evidence(self):
        with tempfile.TemporaryDirectory() as d:
            _,item=self._registered_image(d)
            item['privacy_review']='approved'
            item['publication_approved']=True
            item['rights_evidence']=''
            with self.assertRaisesRegex(ValueError,'Rights evidence'):
                validate_for_render(item)

if __name__=='__main__':
    unittest.main()
