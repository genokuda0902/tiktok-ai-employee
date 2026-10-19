from meter import meter_history

def test_meter_history():
    assert meter_history([0.1, 0.2, 0.3], 2, 2) == [0.2, 0.3]
    assert meter_history([0.1], 0, 3) == [0.1, 0.1, 0.1]
