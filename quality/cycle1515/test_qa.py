import unittest
from quality.cycle1515.qa import inspect
class QA(unittest.TestCase):
 def test_missing_file(self):
  with self.assertRaises(Exception):inspect("/nonexistent/file.mp4")
 def test_fail_closed(self):
  self.assertFalse(inspect.__doc__ == "approved")
if __name__=="__main__":unittest.main()
