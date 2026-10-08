from src.quality.cycle422_plan import GENRES, SCENE_SECONDS, validate


def test_cycle422_contract():
    assert validate()
    assert len(GENRES) == len(set(GENRES)) == 10
    assert len(SCENE_SECONDS) == 7
    assert 15 <= sum(SCENE_SECONDS) <= 25


def test_cycle422_review_status():
    assert validate() is True
