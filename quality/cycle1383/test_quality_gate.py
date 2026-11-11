from quality_gate import publication_allowed, validate_excel_example

def test_unapproved_never_publishes():
    assert not publication_allowed({"video_decodes": True})

def test_valid_excel_example():
    assert validate_excel_example([2000, 3200, 4100, 3100], "=SUM(B2:B5)", 12400)

def test_wrong_formula_fails():
    assert not validate_excel_example([2000, 3200, 4100, 3100], "=SUM(B2-B5)", 12400)
