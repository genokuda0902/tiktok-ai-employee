import pytest

from video_engine.production_v2.hook_evidence_guard import HookEvidence, validate_hook


def valid_hook(**overrides):
    data = dict(
        duration_s=1.2,
        headline="10分→1分",
        evidence_type="before_after",
        has_numeric_or_visual_result=True,
        rights_approved=True,
        contains_personal_data=False,
    )
    data.update(overrides)
    return HookEvidence(**data)


def test_accepts_result_first_approved_hook():
    validate_hook(valid_hook())


@pytest.mark.parametrize("duration_s", [0.39, 1.51])
def test_rejects_hook_outside_first_1_5_seconds(duration_s):
    with pytest.raises(ValueError):
        validate_hook(valid_hook(duration_s=duration_s))


@pytest.mark.parametrize("evidence_type", ["placeholder", "generic_card", ""])
def test_rejects_generic_or_unknown_evidence(evidence_type):
    with pytest.raises(ValueError):
        validate_hook(valid_hook(evidence_type=evidence_type))


def test_rejects_hook_without_result_evidence():
    with pytest.raises(ValueError):
        validate_hook(valid_hook(has_numeric_or_visual_result=False))


def test_rejects_unapproved_rights():
    with pytest.raises(ValueError):
        validate_hook(valid_hook(rights_approved=False))


def test_rejects_personal_data():
    with pytest.raises(ValueError):
        validate_hook(valid_hook(contains_personal_data=True))
