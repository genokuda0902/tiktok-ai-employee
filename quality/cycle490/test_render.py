from render import VALUES, ENDS, CAPTIONS, TITLES

def test_contract():
    assert sum(VALUES)==720
    assert ENDS[-1]==20
    assert len(CAPTIONS)==len(TITLES)==8
