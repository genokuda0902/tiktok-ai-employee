from quality.cycle529_loop_wipe import wipe_frame
import numpy as np

def test_wipe():
    a=np.zeros((2,4,3),dtype=np.uint8)
    b=np.ones((2,4,3),dtype=np.uint8)
    assert np.array_equal(wipe_frame(a,b,0),a)
    assert np.array_equal(wipe_frame(a,b,1),b)
