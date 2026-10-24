import json,unittest
from pathlib import Path
CATALOG=Path(__file__).with_name('genre_catalog819.json')
class TestGenreCatalog(unittest.TestCase):
    def test_ten_genres(self):
        d=json.loads(CATALOG.read_text(encoding='utf8'))
        self.assertEqual(len(d['genres']),10)
        self.assertEqual(d['common']['resolution'],[1080,1920])
        self.assertEqual(d['common']['fps'],30)
        self.assertEqual(d['common']['publication_gate'],'EMPLOYEE_MANUAL_APPROVAL')
    def test_every_genre_has_hook_and_cta(self):
        for key,genre in json.loads(CATALOG.read_text(encoding='utf8'))['genres'].items():
            with self.subTest(genre=key):
                self.assertTrue(genre['hook'] and genre['cta'])
                self.assertRegex(genre['accent'],r'^#[0-9A-F]{6}$')
if __name__=='__main__':unittest.main()
