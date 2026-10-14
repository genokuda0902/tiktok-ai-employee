import unittest

class ReviewGateTests(unittest.TestCase):
    def test_not_approved(self):
        status = 'HUMAN_REVIEW'
        self.assertNotEqual(status, 'PUBLICATION_APPROVED')

if __name__ == '__main__':
    unittest.main()
