"""Reusable ten-genre, synthetic-data evidence mapping. No real AI outcome claimed."""
from dataclasses import dataclass
from evidence_contract import GENRES, validate

@dataclass(frozen=True)
class ProofRow:
    month: int
    cell: str
    value: int
    cumulative: int

def proof_mapping(genre: str, values=(120, 150, 200, 250)):
    validated = validate(genre, values)
    total = 0
    rows = []
    for month, value in enumerate(validated['values'], 1):
        total += value
        rows.append(ProofRow(month, f'B{month+1}', value, total))
    assert total == validated['sum']
    return {'genre': genre, 'rows': rows, 'total': total,
            'formula': '=SUM(B2:B5)', 'synthetic': True,
            'label': GENRES[genre]}

def scene_state(t: float, genre='AI・仕事効率化', values=(120,150,200,250)):
    if not 0 <= t < 3.9:
        raise ValueError('scene time out of range')
    data = proof_mapping(genre, values)
    idx = min(3, int(t / 0.85))
    return {**data, 'highlight_index': idx, 'all_values_visible': True,
            'sum_visible': True, 'formula_visible': True}

def caption_bounds_ok(box, size=(540,960)):
    x0,y0,x1,y1=box
    return 22<=x0<x1<=480 and 95<=y0<y1<=815
