from evidence_motion import DEMO, bar_state

def check():
    assert DEMO.validate()
    assert bar_state(DEMO,119)['total']==720
    assert bar_state(DEMO,0)['total'] is None

if __name__=='__main__':
    check()
    print('PASS')
