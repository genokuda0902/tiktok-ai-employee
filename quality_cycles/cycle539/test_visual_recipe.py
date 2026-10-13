"""No-media unit tests for the cycle539 reusable renderer."""
import numpy as np
from visual_recipe import GENRES, warp_subject, feathered_zone

def test_genre_count():
    assert len(GENRES)==10 and len(set(GENRES))==10

def test_perspective_rgba():
    sample=np.zeros((40,80,3),dtype=np.uint8);sample[:]=[10,100,80]
    im=warp_subject(sample,[[5,5],[70,10],[75,40],[10,45]],(90,60))
    assert im.mode=='RGBA' and im.size==(90,60)
    assert max(im.getchannel('A').getextrema())==255

def test_feathered_zone():
    a=feathered_zone(1080,835)
    assert a.shape==(835,1080)
    assert a[400,500]>0.99 and a[0,500]<0.5
