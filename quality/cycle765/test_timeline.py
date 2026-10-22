from prompt_timeline import STAGES, GENRES, prompt_at

def test_stages():
    assert sum(b-a+1 for a,b in STAGES)==105
    assert len(GENRES)==10
    assert prompt_at(0)==''
