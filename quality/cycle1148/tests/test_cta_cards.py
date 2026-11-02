import hashlib,tempfile,unittest
from pathlib import Path
from PIL import Image
from cta_cards import GENRES,ROI,CAPTION_START,POLICY,make_card_strip,check

class TestCtaCards(unittest.TestCase):
 def setUp(self):
  self.tmp=tempfile.TemporaryDirectory();self.src=Path(self.tmp.name)/'source.mp4'
  self.src.write_bytes(b'fixture')
  self.data={'policy':POLICY,'genre':'ai','source_sha256':hashlib.sha256(b'fixture').hexdigest(),
   'asset_approval':'review_only_original_graphics','steps':[20.55,20.95,21.55,23.03]}
 def tearDown(self):self.tmp.cleanup()
 def test_ten_genres(self):
  for genre in GENRES:
   self.data['genre']=genre
   self.assertEqual(check(self.data,self.src,23.033),self.data['steps'])
   for i in range(3):
    p=Path(self.tmp.name)/f'{genre}{i}.png';make_card_strip(genre,i,p)
    with Image.open(p) as im:self.assertEqual(im.size,ROI[2:])
 def test_policy(self):
  self.data['policy']='PUBLICATION_APPROVED'
  with self.assertRaises(ValueError):check(self.data,self.src,23.033)
 def test_hash(self):
  self.data['source_sha256']='0'*64
  with self.assertRaises(ValueError):check(self.data,self.src,23.033)
 def test_rights(self):
  del self.data['asset_approval']
  with self.assertRaises(ValueError):check(self.data,self.src,23.033)
 def test_time(self):
  self.data['steps']=[19,20,21,23.03]
  with self.assertRaises(ValueError):check(self.data,self.src,23.033)
 def test_caption(self):self.assertLess(ROI[1]+ROI[3],CAPTION_START)
 def test_distinct_states(self):
  paths=[]
  for i in range(3):
   p=Path(self.tmp.name)/f'{i}.png';make_card_strip('ai',i,p);paths.append(p)
  self.assertEqual(len({hashlib.sha256(p.read_bytes()).hexdigest() for p in paths}),3)
if __name__=='__main__':unittest.main()
