import unittest
from validate_srt import validate

def sample(overlap=False):
    blocks = []
    for i in range(8):
        start = i * 2 if not overlap or i != 4 else 7
        def ts(s): return f"00:00:{s:02d},000"
        blocks.append(f"{i+1}\\n{ts(start)} --> {ts(start+1)}\\n字幕{i+1}")
    return "\\n\\n".join(blocks).replace("\\n","\n")

class TestSrt(unittest.TestCase):
    def test_valid(self): self.assertTrue(validate(sample(), 22.23))
    def test_overlap(self):
        with self.assertRaises(ValueError): validate(sample(True), 22.23)
    def test_wrong_duration(self):
        with self.assertRaises(ValueError): validate(sample(), 10)
    def test_wrong_count(self):
        with self.assertRaises(ValueError): validate(sample(), 22.23, 7)

if __name__ == "__main__": unittest.main()
