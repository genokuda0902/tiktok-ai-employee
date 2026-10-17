from PIL import Image, ImageOps


def test_preserve_ratio():
    source = Image.new('RGB', (940, 590))
    fitted = ImageOps.contain(source, (880, 630))
    assert abs(source.width/source.height - fitted.width/fitted.height) < 0.004
