from detail import render
import inspect

def test_subtitle_region_protected():
    code=inspect.getsource(render)
    assert 'crop=iw:1380' in code
    assert 'unsharp=5:5:0.35' in code
    assert 'copy' in code
