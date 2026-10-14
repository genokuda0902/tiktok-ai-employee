"""Reusable cycle580 proof graphics; review-only synthetic data."""
import math
from PIL import Image, ImageDraw, ImageFont
GENRES = ('ai_productivity', 'beauty', 'relationships', 'finance', 'sales',
          'career', 'wellness', 'science', 'travel_food', 'product_comparison')
VALUES = (120, 150, 200, 250)
FPS, WIDTH, HEIGHT = 30, 1080, 1920
START, END = 9, 12
FONT = '/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc'
BOLD = '/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc'

def check(genre='ai_productivity', values=VALUES, total=720):
    if genre not in GENRES:
        raise ValueError('unknown genre')
    if len(values) != 4 or any(type(v) is not int or v < 0 for v in values):
        raise ValueError('four nonnegative integers required')
    if sum(values) != total:
        raise ValueError('proof total does not match evidence')
    return True

def rounded(draw, box, radius, fill, outline=None, width=2):
    draw.rounded_rectangle(box, radius, fill=fill, outline=outline, width=width)

def build_frame(base, frame_index, values=VALUES):
    """All overlaid proof labels >=44px at 1080 width; no source media copied."""
    check(values=values, total=sum(values))
    t = frame_index / FPS
    im = base.copy().convert('RGB')
    d = ImageDraw.Draw(im)
    # Only the central proof panel is replaced. Existing title/caption stay put.
    rounded(d, (25, 153, 1055, 1655), 38, '#06192a', '#2f8aa5', 4)
    rounded(d, (63, 193, 1017, 348), 24, '#103b52', '#55d4e0', 3)
    d.text((91, 218), '4か月の売上 → 合計を検算', font=ImageFont.truetype(BOLD, 55), fill='#ffffff')
    d.text((91, 294), '数字の出所と計算式を同時に表示', font=ImageFont.truetype(FONT, 29), fill='#9ce7ed')
    rounded(d, (65, 378, 532, 1254), 25, '#eaf5f6', '#4bd1cc', 4)
    rounded(d, (565, 378, 1016, 1254), 25, '#0d3047', '#56cdd3', 4)
    d.text((92, 408), '元データ（架空）', font=ImageFont.truetype(BOLD, 42), fill='#124155')
    d.text((600, 408), 'SUMで検算', font=ImageFont.truetype(BOLD, 42), fill='#ffffff')
    d.text((96, 495), 'セル', font=ImageFont.truetype(BOLD, 35), fill='#3b5968')
    d.text((335, 495), '売上', font=ImageFont.truetype(BOLD, 35), fill='#3b5968')
    for i, val in enumerate(values):
        y = 567 + i * 142
        rounded(d, (90, y, 502, y + 119), 14, '#ffffff' if i % 2 == 0 else '#d8eef0')
        d.text((118, y + 17), f'B{i+2}', font=ImageFont.truetype(BOLD, 60), fill='#143e4f')
        if t > 0.12 + i * 0.13:
            d.text((332, y + 17), str(val), font=ImageFont.truetype(BOLD, 62), fill='#0b5c65')
    if t >= 0.8:
        pulse = int(3 * math.sin((t-0.8) * 7))
        rounded(d, (310, 558, 502, 1126), 15, None, '#30e5b4', 7 + max(0, pulse))
        rounded(d, (327, 1142, 492, 1213), 12, '#006d65')
        d.text((342, 1146), 'B2:B5', font=ImageFont.truetype(BOLD, 37), fill='white')
    rounded(d, (590, 502, 991, 638), 18, '#e6f8fa')
    formula = '=SUM(B2:B5)'
    shown = formula[:max(0, min(len(formula), int((t-1.2)*17)))] if t < 2.15 else formula
    if t >= 1.1:
        d.text((609, 537), shown, font=ImageFont.truetype(BOLD, 43), fill='#0d3b50')
    else:
        d.text((614, 541), '範囲を選択', font=ImageFont.truetype(BOLD, 39), fill='#426779')
    rounded(d, (590, 704, 991, 987), 20, '#07534d' if t >= 2.15 else '#123d50', '#52e2d1', 3)
    d.text((617, 735), '検算した合計', font=ImageFont.truetype(BOLD, 42), fill='#d9fbf7')
    if t >= 2.15:
        d.text((668, 801), str(sum(values)), font=ImageFont.truetype(BOLD, 107), fill='#ffffff')
    else:
        d.text((639, 822), '計算中…', font=ImageFont.truetype(BOLD, 53), fill='#b3d7df')
    rounded(d, (594, 1054, 989, 1197), 14, '#0d2539', '#277a8b', 2)
    d.text((618, 1083), '120 + 150 + 200 + 250', font=ImageFont.truetype(BOLD, 29), fill='#c4eaf0')
    d.text((618, 1134), '= 720', font=ImageFont.truetype(BOLD, 42), fill='#6cf1c2')
    for idx, (label, active_at) in enumerate([('① 元データ',0.0),('② 範囲選択',0.8),('③ SUMで検算',2.15)]):
        left=76+idx*320
        rounded(d,(left,1408,left+300,1519),16, '#11665b' if t>=active_at else '#18384b',
                '#4fe2c0' if t>=active_at else '#3e6e7d', 3)
        d.text((left+20,1437),label,font=ImageFont.truetype(BOLD,35),fill='#ffffff')
    d.text((83, 1572), '※操作再現・架空データ／実際のExcel録画ではありません',
           font=ImageFont.truetype(FONT, 26), fill='#c0d5e2')
    return im

