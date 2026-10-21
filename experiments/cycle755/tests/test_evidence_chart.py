from pathlib import Path
import importlib.util
import pytest
p=Path(__file__).resolve().parents[1]/'src/evidence_chart.py'
spec=importlib.util.spec_from_file_location('evidence_chart',p)
m=importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)
def test_ten_genres():
    assert len(m.GENRES)==10
    for genre in m.GENRES:
        assert m.validate(genre=genre)==65
        assert m.frame_image(60,genre=genre).size==(924,720)
def test_values():
    assert m.validate()==65
    with pytest.raises(ValueError):m.validate((('A',5),('A',6)))
    with pytest.raises(ValueError):m.validate((('A',-5),('B',6)))
def test_progress():
    assert m.progress(10,3)==0
    assert m.progress(65,3)==1
def test_alpha():
    assert m.frame_image(0).getchannel('A').getextrema()==(0,0)
    assert m.frame_image(35).getchannel('A').getextrema()[1]>200
