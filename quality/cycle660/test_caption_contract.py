from quality.cycle660.cycle660_common import GENRES, break_caption, validate_contract

def test_ten_genres():
    assert len(GENRES) == 10

def test_caption_rejects_empty():
    try:
        break_caption('', len, 10)
    except ValueError:
        return
    assert False

def test_timeline():
    assert validate_contract([{'start': 0, 'end': 1, 'spoken_text': 'ok'}], 'science') == 1
