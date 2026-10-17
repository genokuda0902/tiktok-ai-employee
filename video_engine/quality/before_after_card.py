"""Illustrative comparison card; not an actual software operation recording."""
from PIL import ImageDraw

def draw_before_after(im, text, *, before='手作業', after='AI下書き',
                      checks=('転記', '集計', 'グラフ'), disclaimer='※ AI出力は必ず検算'):
    d = ImageDraw.Draw(im)
    d.rounded_rectangle((35, 248, 505, 659), radius=22, fill='#eaf8ff')
    d.rounded_rectangle((49, 271, 262, 581), radius=18, fill='#f3e5e7')
    d.rounded_rectangle((279, 271, 491, 581), radius=18, fill='#e2fff2')
    text(d, 74, 291, 'BEFORE', 23, '#8c3a4d')
    text(d, 303, 291, 'AFTER', 23, '#116b57')
    text(d, 78, 352, before, 35, '#6d3445')
    text(d, 297, 352, after, 31, '#116b57')
    for k, label in enumerate(checks[:3]):
        yy = 424 + k * 45
        text(d, 92, yy, label, 21, '#684552')
        text(d, 323, yy, '✓ ' + label, 21, '#136955')
    text(d, 94, 610, disclaimer, 24, '#194a60')
    return {'illustrative_only': True, 'disclaimer': disclaimer}
