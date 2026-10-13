"""Spreadsheet evidence validation, review-only."""
FORMULA = "=SUM(B2:B5)"
def check(values):
    if len(values) != 4 or any(type(v) is not int or v < 0 for v in values):
        raise ValueError("expected four nonnegative integers")
    return {"B2": values[0], "B3": values[1], "B4": values[2], "B5": values[3], "B6": sum(values)}
