import hook_spec

def test_hook_dimensions():
    assert hook_spec.validate()

def test_caption():
    assert hook_spec.caption_at(0.5) == 'この基板、'
