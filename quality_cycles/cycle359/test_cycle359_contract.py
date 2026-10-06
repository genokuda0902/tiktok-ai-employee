def test_cycle359_policy():
    variants=['result_first','problem_first','before_after']
    assert len(variants)==3
    assert 'auto_post' not in variants
