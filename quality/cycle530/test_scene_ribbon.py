import hashlib
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch
from quality.cycle530 import scene_ribbon as m

class TestSceneRibbon(unittest.TestCase):
    def test_ten_genres_and_gates(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)/'synthetic';p.write_bytes(b'owner-approved synthetic')
            manifest={'genre':m.GENRES[0], 'rights':'SYNTHETIC_OR_OWNER_APPROVED',
              'contains_private_data':False,'publication':'NOT_APPROVED',
              'review_status':'HUMAN_REVIEW','japanese_narration':'NOT_GENERATED',
              'source_sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
            with patch.object(m,'FONT',str(p)):
                self.assertEqual(len(m.GENRES),10)
                for genre in m.GENRES:
                    manifest['genre']=genre
                    m.validate_manifest(manifest,p)
                for key,value in [('rights','UNKNOWN'),('contains_private_data',True),
                    ('publication','APPROVED'),('japanese_narration','GENERATED'),
                    ('source_sha256','0'*64)]:
                    bad=dict(manifest);bad[key]=value
                    with self.assertRaises(ValueError):m.validate_manifest(bad,p)
    def test_four_nonoverlapping_stages(self):
        self.assertEqual(len(m.STAGES),4)
        self.assertEqual(m.make_filter().count('drawbox='),8)
        with self.assertRaises(ValueError):
            m.make_filter(((2.5,5,'課題'),(4,10,'操作'),(10,15,'結果'),(15,17.5,'確認')))

if __name__=='__main__':unittest.main()
