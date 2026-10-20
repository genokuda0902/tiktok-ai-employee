from prompt_motion import state_at

def test_send_gate():
    assert state_at(2.4).sent is False
    assert state_at(2.9).sent is True
