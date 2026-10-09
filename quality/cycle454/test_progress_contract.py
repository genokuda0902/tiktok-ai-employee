from progress_contract import PHASES,VOICE_SEGMENTS,validate,phase_at,PUBLICATION

def test_timeline():
    assert validate()
    assert phase_at(8)==1
    assert phase_at(14)==2
    assert len(VOICE_SEGMENTS)==7
    assert PUBLICATION=='NOT_APPROVED'
