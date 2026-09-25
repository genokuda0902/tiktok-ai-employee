import unittest
from video_engine.deterministic_ui_layer import SpreadsheetRow, validate_rows, release_contract

class DeterministicUILayerTests(unittest.TestCase):
    def test_valid_rows(self):
        rows=[SpreadsheetRow("4/1","商品A",125000,12),SpreadsheetRow("4/1","商品B",98000,8),SpreadsheetRow("4/2","商品A",142000,15)]
        validate_rows(rows)

    def test_blank_text_fails_closed(self):
        with self.assertRaises(ValueError):
            validate_rows([SpreadsheetRow("","商品A",1,1)]*3)

    def test_negative_values_fail_closed(self):
        with self.assertRaises(ValueError):
            validate_rows([SpreadsheetRow("4/1","商品A",-1,1)]*3)

    def test_release_policy(self):
        c=release_contract()
        self.assertTrue(c["zero_cost"])
        self.assertTrue(c["deterministic_text_layer"])
        self.assertFalse(c["ai_generated_ui_text_allowed"])
        self.assertEqual(c["portrait_delivery"], (1080,1920))
        self.assertTrue(c["manual_post_only"])
        self.assertFalse(c["auto_post"])

if __name__=="__main__":
    unittest.main()
