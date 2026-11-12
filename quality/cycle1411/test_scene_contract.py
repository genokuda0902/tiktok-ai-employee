import unittest
from scene_contract import SCENES,validate,at
class TestSceneContract(unittest.TestCase):
    def test_timing(self):
        self.assertEqual(validate(SCENES),12)
        self.assertEqual([at(t)[0] for t in (0,2.99,3,5.99,6,9,11.99)],[0,0,1,1,2,3,3])
    def test_fail_closed(self):
        with self.assertRaises(ValueError): validate([{"seconds":2,"caption":""}])
        with self.assertRaises(ValueError): at(-1)
if __name__=="__main__": unittest.main()
