"""Tests for the reusable ten-genre slide configuration."""

def test_ten_unique_genres(genres):
    names = [g['name'] for g in genres['genres']]
    assert len(names) == len(set(names)) == 10


def test_each_genre_has_a_visual_format(genres):
    assert all(g['format'] and g['primary_response'] for g in genres['genres'])
