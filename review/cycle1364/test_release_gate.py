from release_gate import release_gate

def test_fail_closed():
    assert not release_gate(False, True, True)
    assert not release_gate(True, False, True)
    assert not release_gate(True, True, False)

def test_only_all_verified_pass():
    assert release_gate(True, True, True)
