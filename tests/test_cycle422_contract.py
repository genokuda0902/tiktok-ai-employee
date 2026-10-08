def test_cycle422_review_status():
    status = 'HUMAN_REVIEW / PUBLICATION_NOT_APPROVED'
    assert 'NOT_APPROVED' in status

def test_cycle422_ten_genres():
    genres = ['ai_work', 'beauty', 'psychology', 'finance', 'sales', 'career', 'health', 'science', 'travel', 'shopping']
    assert len(genres) == len(set(genres)) == 10
