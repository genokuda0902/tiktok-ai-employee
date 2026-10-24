import importlib.util, unittest
from pathlib import Path
p=Path(__file__).with_name('make_japanese_fixture819.py')
spec=importlib.util.spec_from_file_location('voice819',p)
m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
class TestJapaneseFixture(unittest.TestCase):
    def test_atempo_normal(self):
        self.assertEqual(m.atempo_chain(1.0),'atempo=1.0000000')
    def test_atempo_high(self):
        self.assertEqual(m.atempo_chain(3.0),'atempo=2.0,atempo=1.5000000')
    def test_atempo_invalid(self):
        with self.assertRaises(ValueError):m.atempo_chain(0.8)
    def test_attribution(self):
        self.assertIn('CC BY 3.0',m.CREDIT)
        self.assertIn('Nagoya Institute',m.CREDIT)
    def test_no_upload(self):
        t=p.read_text(encoding='utf8')
        for s in ['tiktok.upload(', 'requests.post(', 'openai.api_key']:
            self.assertNotIn(s,t)
if __name__=='__main__':unittest.main()
