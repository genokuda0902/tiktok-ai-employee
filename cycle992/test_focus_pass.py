import unittest
from focus_pass import validate,filtergraph

CFG={'genre':'test','review_only':True,'publication_approved':False,
     'beats':[{'start':0.2,'end':0.8,'x':40,'y':50,'w':200,'h':90},
              {'start':0.9,'end':1.6,'x':40,'y':160,'w':200,'h':90}]}

class TestFocus(unittest.TestCase):
    def test_valid(self): self.assertEqual(len(validate(CFG)),2)
    def test_filter(self):
        s=filtergraph(CFG)
        self.assertEqual(s.count('drawbox='),4)
        self.assertIn('between(t\\,0.200\\,0.800)',s)
    def test_review_gate(self):
        with self.assertRaises(ValueError): validate({**CFG,'publication_approved':True})
    def test_missing_genre(self):
        with self.assertRaises(ValueError): validate({**CFG,'genre':None})
    def test_caption_safe(self):
        c={**CFG,'beats':[{**CFG['beats'][0],'y':1240,'h':100},CFG['beats'][1]]}
        with self.assertRaises(ValueError): validate(c)
    def test_overlap(self):
        c={**CFG,'beats':[CFG['beats'][0],{**CFG['beats'][1],'start':0.7}]}
        with self.assertRaises(ValueError): validate(c)
    def test_source_safe(self):
        c={**CFG,'beats':[{**CFG['beats'][0],'x':1050},CFG['beats'][1]]}
        with self.assertRaises(ValueError): validate(c)
    def test_minimum(self):
        with self.assertRaises(ValueError): validate({**CFG,'beats':[CFG['beats'][0]]})

if __name__=='__main__': unittest.main()
