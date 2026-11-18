from pathlib import Path
from tempfile import TemporaryDirectory
from normalize import normalize

def test_missing_input():
    with TemporaryDirectory() as d:
        try:
            normalize(Path(d)/'missing.mp4',Path(d)/'out.mp4')
        except FileNotFoundError:
            return
        raise AssertionError('missing source must fail')

def test_filter_parameters():
    import inspect
    assert 'I=-16:TP=-1.5:LRA=11' in inspect.getsource(normalize)
    assert "'-c:v','copy'" in inspect.getsource(normalize)
