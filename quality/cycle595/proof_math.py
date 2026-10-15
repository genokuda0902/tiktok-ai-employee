"""Verified synthetic proof totals for cycle595."""

def verified_total(values):
    if len(values) != 4:
        raise ValueError('four inputs required')
    return sum(values)
