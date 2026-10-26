"""Portable 10-genre content-first visual grammar for vertical short-form videos.

This module contains no media or private data. CI tests layout invariants, not
Japanese voice rights, subjective quality, or private MP4 reproducibility.
"""
from dataclasses import dataclass

WIDTH, HEIGHT, FPS = 1080, 1920, 30
CAPTION_BAND = (76, 1510, 1003, 1820)
VISUAL_BAND = (72, 615, 1008, 1300)
PALETTES = {
 'ai_productivity': ('#635BFF','#10BFA9'),
 'beauty': ('#DF5E9D','#F8ABCE'),
 'romance_psychology': ('#C76AA7','#F5A5C6'),
 'money_saving': ('#21866C','#9DDBB3'),
 'sales_business': ('#2D6AC4','#6AC1F5'),
 'career': ('#6B63C6','#A4A8FA'),
 'health_lifestyle': ('#008FA7','#7BD1D6'),
 'trivia_science': ('#8055BC','#C3A2EF'),
 'travel_food': ('#287BB6','#82D7EE'),
 'product_lifestyle': ('#C98032','#EFC48A'),
}
@dataclass(frozen=True)
class Scene:
    headline: tuple[str,str]
    supporting: str
    pictogram: str

SCENES = (
 Scene(('AIで仕事を','もっと軽く。'),'今日から使える、仕事の整え方','spark'),
 Scene(('まず、毎日の','作業を書き出す'),'繰り返しを見つけるのが最初の一歩','check'),
 Scene(('完成形の','見本を用意'),'「何を作りたいか」を見える形に','document'),
 Scene(('目的と条件を','具体的に伝える'),'曖昧な指示から、伝わる指示へ','target'),
 Scene(('最初の出力は','必ず自分で確認'),'数字・表現・抜け漏れをチェック','inspect'),
 Scene(('違いがあれば','ひとつずつ修正'),'直したい箇所を具体的に伝える','edit'),
 Scene(('使える指示は','テンプレに残す'),'次回はゼロから考えない','save'),
 Scene(('小さな時短を','毎日の習慣に'),'保存して、次の仕事で試してみよう','habit'),
)

def inside(box, outer=(0,0,WIDTH,HEIGHT)):
    x0,y0,x1,y1=box; a,b,c,d=outer
    return a<=x0<x1<=c and b<=y0<y1<=d

def validate(genre='ai_productivity'):
    if genre not in PALETTES: raise ValueError('Unknown genre')
    if len(SCENES)!=8: raise ValueError('Expected 8 scenes')
    if not inside(CAPTION_BAND) or not inside(VISUAL_BAND): raise ValueError('Out of bounds')
    if VISUAL_BAND[3]>=CAPTION_BAND[1]: raise ValueError('Caption/visual collision')
    if len({s.pictogram for s in SCENES})!=8: raise ValueError('Pictograms not unique')
    if any('75%' in ' '.join(s.headline)+s.supporting for s in SCENES):
        raise ValueError('Unsupported performance claim')
    return True
