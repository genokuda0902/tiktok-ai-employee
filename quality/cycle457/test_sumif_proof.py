import pytest
from sumif_proof import (ROWS, SCENES, SUMIF_FORMULA, QualityState,
                         team_totals, stage_at, validate_proof, release_gate)

def test_synthetic_totals():
    assert team_totals() == {"A": 35, "B": 26}
def test_total_61():
    assert sum(team_totals().values()) == 61
def test_formula():
    assert SUMIF_FORMULA == '=SUMIF(B4:B9,"A",C4:C9)'
def test_rows():
    assert validate_proof() == {"A": 35, "B": 26}
def test_modified_data_rejected():
    bad = list(ROWS)
    bad[0] = ("04/01", "A", 100)
    with pytest.raises(ValueError): validate_proof(bad)
def test_duplicate_data_rejected():
    with pytest.raises(ValueError): validate_proof([ROWS[0]]*6)
@pytest.mark.parametrize("t,stage", [
    (0,"HOOK"), (2,"INPUT"), (5,"TRANSFORM"),
    (9,"PROOF"), (12,"RESULT"), (15,"COMPARE"), (18,"CTA")
])
def test_stage(t,stage):
    assert stage_at(t) == stage
def test_out_of_bounds():
    with pytest.raises(ValueError): stage_at(20)
def test_narration_missing():
    assert release_gate(QualityState()) == "REVIEW_ONLY_NARRATION_MISSING"
def test_sync_missing():
    assert release_gate(QualityState(japanese_voice_verified=True)) == "REVIEW_ONLY_SYNC_UNVERIFIED"
def test_human_review():
    assert release_gate(QualityState(japanese_voice_verified=True,semantic_caption_sync_verified=True)) == "HUMAN_REVIEW_REQUIRED"
def test_autopost_forbidden():
    with pytest.raises(ValueError): release_gate(QualityState(auto_post=True))
def test_approval_forbidden():
    with pytest.raises(ValueError): release_gate(QualityState(publication="APPROVED"))
def test_rights_required():
    with pytest.raises(ValueError): release_gate(QualityState(rights="UNKNOWN"))
