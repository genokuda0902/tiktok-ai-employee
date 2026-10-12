from quality.cycle518.proof_state_consistency import STATES


def test_states():
    assert STATES == ('input', 'calculating', 'verified')
