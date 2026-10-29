import sys
from pathlib import Path
import pytest
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'src'))
from evidence_consistency import (GENRES, Evidence, make_ai_work_evidence,
                                  semantic_gate, filtergraph, BAND_PHASE1, BAND_PHASE2, CAPTION_TOP,
                                  PHASE1, PHASE2, validate_source)


def test_valid_evidence():
    x = make_ai_work_evidence()
    x.validate()
    assert x.total_a == 46 and x.total_b == 29

@pytest.mark.parametrize('genre', GENRES)
def test_genre_can_be_validated_but_not_auto_approved(genre):
    e = Evidence(genre, True, False, (2,3), (4,5), 5, 9, 'demo')
    e.validate()
    assert e.approved_for_publication is False

@pytest.mark.parametrize('a,b,ta,tb', [((12,16,18),(8,9,12),45,29),
                                      ((12,16,18),(8,9,12),46,28),
                                      ((12,16),(8,9,12),28,29),
                                      ((True,16,18),(8,9,12),35,29),
                                      ((-1,16,18),(8,9,12),33,29)])
def test_reject_bad_arithmetic(a,b,ta,tb):
    with pytest.raises(ValueError):
        Evidence('ai_work',True,False,a,b,ta,tb,'demo').validate()

@pytest.mark.parametrize('genre,fictional,approved', [
    ('unknown',True,False),('ai_work',False,False),('ai_work',True,True)])
def test_reject_unsafe_metadata(genre,fictional,approved):
    with pytest.raises(ValueError):
        Evidence(genre,fictional,approved,(2,3),(4,5),5,9,'demo').validate()

@pytest.mark.parametrize('transcript,caption,asr,expected', [
    (None,'音声あり',False,'UNVERIFIED'),
    ('こんにちは','こんにちは',False,'UNVERIFIED'),
    ('こんにちは。','こんにちは',True,'TEXT_MATCH_ONLY'),
    ('元データと確認','元データを確認',True,'MISMATCH'),
])
def test_semantic_gate_does_not_fake_asr(transcript,caption,asr,expected):
    result = semantic_gate(transcript=transcript,caption=caption,independent_asr=asr,employee_approved=False)
    assert result['semantic_status'] == expected
    assert result['publication_allowed'] is False


def test_approval_alone_never_authorizes_posting():
    x = semantic_gate(transcript='同じ',caption='同じ',independent_asr=True,employee_approved=True)
    assert x['publication_allowed'] is False


def test_cue_safe_from_subtitles_and_chronological():
    assert BAND_PHASE1[1] + BAND_PHASE1[3] < CAPTION_TOP
    assert BAND_PHASE2[1] + BAND_PHASE2[3] < CAPTION_TOP
    assert PHASE1[1] == PHASE2[0]
    assert 0 <= PHASE1[0] < PHASE2[1] < 691/30


def test_filtergraph_uses_two_review_phases(tmp_path):
    font = tmp_path/'font.ttc'; a=tmp_path/'one.txt'; b=tmp_path/'two.txt'
    x=filtergraph(a,b,font)
    assert 'between(t,11.75,13.45)' in x
    assert 'between(t,13.45,14.35)' in x
    assert 'drawtext' in x and 'drawbox' in x
    assert 'publish' not in x


def test_missing_source_rejected(tmp_path):
    with pytest.raises(ValueError):
        validate_source(tmp_path/'absent.mp4','a'*64,make_ai_work_evidence())
