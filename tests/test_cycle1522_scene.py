from cycle1522_scene import scene_at, publication_allowed
import pytest

def test_boundaries():
    assert [scene_at(t) for t in (0, 3, 6, 9, 11.9)] == [0, 1, 2, 3, 3]

def test_outside():
    with pytest.raises(ValueError):
        scene_at(12)

def test_fail_closed():
    assert not publication_allowed(True, True, True, True)
