"""Offline unit tests for the same photo-story module used for cycle849 MP4."""
import json
import tempfile
import unittest
from pathlib import Path
from PIL import Image
from photo_story import GENRES, REVIEW_ONLY, SCENES, W, H, validate, make_slide, make_ass

class PhotoStoryTests(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root=Path(self.tmp.name)
        self.photos=[]
        for i in range(8):
            p=self.root/f'{i}.jpg'
            Image.new('RGB',(820,860),(20+i*20,50,80)).save(p)
            self.photos.append(p)
        self.beats=[{'start':i*0.9,'end':i*0.9+0.8,'text':f'字幕{i}'} for i in range(24)]
    def test_ten_genres(self):
        self.assertEqual(len(GENRES),10)
        for genre in GENRES:self.assertTrue(validate(genre,self.beats,self.photos))
    def test_review_only_policy(self):
        self.assertEqual(REVIEW_ONLY,dict.fromkeys(REVIEW_ONLY,False))
    def test_eight_scenes(self):
        self.assertEqual(len(SCENES),8)
    def test_invalid_genre(self):
        with self.assertRaises(ValueError):validate('unsupported',self.beats,self.photos)
    def test_missing_photo(self):
        with self.assertRaises(ValueError):validate('ai_work',self.beats,self.photos[:7])
    def test_missing_caption(self):
        with self.assertRaises(ValueError):validate('ai_work',self.beats[:23],self.photos)
    def test_overlap(self):
        bad=[dict(x) for x in self.beats];bad[1]['start']=0.1
        with self.assertRaises(ValueError):validate('ai_work',bad,self.photos)
    def test_slide_size(self):
        self.assertEqual(make_slide(self.photos[0],0,GENRES['ai_work']).size,(W,H))
    def test_photo_changes_pixels(self):
        a=make_slide(self.photos[0],0,GENRES['ai_work'])
        b=make_slide(self.photos[1],0,GENRES['ai_work'])
        self.assertNotEqual(a.getpixel((500,700)),b.getpixel((500,700)))
    def test_ass_24_events(self):
        p=self.root/'captions.ass';make_ass(self.beats,p)
        content=p.read_text(encoding='utf-8')
        self.assertEqual(content.count('Dialogue: 0,'),24)
        self.assertIn('pos(540,1500)',content)
        self.assertIn('PlayResX: 1080',content)

if __name__=='__main__':unittest.main()
