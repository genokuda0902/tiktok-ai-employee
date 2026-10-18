from quality.cycle666.hook_contract import Scene, validate_scenes, validate_caption_bbox, opening_hook_label


def test_ten_genre_contract():
    genres = tuple('genre_%02d' % i for i in range(10))
    validate_scenes([Scene(0, 1, '日本語', 'slide.png')], genres)


def test_caption_safe_area():
    validate_caption_bbox((56, 1439, 870, 1675))


def test_opening_hook():
    assert opening_hook_label('パソコン') == 'これ、パソコン？'
