from process import render
import inspect

def test_filter_is_reusable():
    s=inspect.getsource(render)
    assert 'crop=iw:180:0:1330' in s
    assert "'-c:a','copy'" in s
    assert "'+faststart'" in s
