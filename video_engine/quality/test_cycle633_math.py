import unittest
from cycle633_spreadsheet_ui import cells, selected_cells, proof, publication_gate
class TestCycle633Math(unittest.TestCase):
    def test_cells(self):
        self.assertEqual([c.address for c in cells()], ['B2','B3','B4','B5'])
    def test_progression(self):
        self.assertEqual([len(selected_cells(x)) for x in (0,.25,.5,1)], [1,2,3,4])
    def test_result(self):
        self.assertEqual(proof(), ('=SUM(B2:B5)',720))
    def test_gate(self):
        self.assertEqual(publication_gate(), 'PUBLICATION_NOT_APPROVED')
