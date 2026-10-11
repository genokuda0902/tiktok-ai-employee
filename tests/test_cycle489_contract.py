import sys
sys.path.insert(0,'quality/cycle489')
from contract import validate

def test_evidence():
    assert validate()
