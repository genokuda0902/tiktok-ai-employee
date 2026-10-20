import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from story_contract import *

def test_sales_proof():
    assert validate_story()
    assert evidence()['peak_month'] == '3月'
    assert evidence()['peak_yen'] == 200000
    assert evidence()['feb_to_mar_growth_pct'] == 33.3

def test_ten_genres():
    assert len(GENRE_SLOTS) == 10
    assert len(set(GENRE_SLOTS)) == 10

def test_timeline_contiguous():
    assert SCENES[0][0] == 0 and SCENES[-1][1] == 20
    assert all(SCENES[i][1] == SCENES[i+1][0] for i in range(7))

def test_assets_fail_closed():
    assert asset_gate([]) is False
    assert asset_gate([{'origin':'reference_video','approved':True}]) is False
    assert asset_gate([{'origin':'self_generated','approved':False}]) is False
    assert asset_gate([{'origin':'self_generated','approved':True}]) is True

def test_publication_fail_closed():
    ok = dict(source_approved=True,privacy_checked=True,employee_approved=True,
              narration_verified=True,captions_synced=True,phone_checked=True)
    assert can_publish(**ok)
    for key in ok:
        denied = dict(ok); denied[key] = False
        assert not can_publish(**denied)
