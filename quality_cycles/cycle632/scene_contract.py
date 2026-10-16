"""Cycle632: ten-genre scene timeline and publication safety gate (stdlib only).
The full executable renderer and generated MP4 are distributed as the cycle632
local QA bundle; this contract is independently CI-testable.
"""
GENRES = {
 'ai_productivity': 'AI仕事術', 'trivia': '雑学', 'cooking': '料理',
 'beauty': '美容', 'money': 'お金', 'health': '健康',
 'travel': '旅行', 'products': '商品比較', 'story': 'ストーリー',
 'work_tips': '仕事のコツ',
}
FPS=30
SCENES=(
 (0,60,'まだ手で集計してる？','hook'),
 (60,120,'4つの数字を確認','problem'),
 (120,180,'必要なのは、この式','solution'),
 (180,270,'B2からB5まで選択','select'),
 (270,360,'SUM関数を入力','formula'),
 (360,450,'合計は720','proof'),
 (450,540,'手作業から数式へ','compare'),
 (540,600,'保存して次回試そう','cta'),
)
VALUES=(120,150,200,250)
def validate(genre='ai_productivity',scenes=SCENES,values=VALUES,asset_manifest=None):
    if genre not in GENRES or len(GENRES)!=10: raise ValueError('genre contract')
    if len(values)!=4 or sum(values)!=720: raise ValueError('synthetic proof mismatch')
    if not 6<=len(scenes)<=10: raise ValueError('scene count')
    if scenes[0][0]!=0 or scenes[-1][1]!=600: raise ValueError('timeline bounds')
    for i,(start,end,caption,kind) in enumerate(scenes):
        if end-start<30 or len(caption)>20: raise ValueError('caption timing/length')
        if i and start!=scenes[i-1][1]: raise ValueError('timeline discontinuity')
    for asset in asset_manifest or []:
        if not (asset.get('approved_for_publication') is True and asset.get('license') and asset.get('source')):
            raise PermissionError('asset not approved')
    return True
def publication_gate(voice_generated=False,speech_sync_verified=False,rights_verified=False,
                     device_verified=False,employee_approved=False):
    if not all((voice_generated,speech_sync_verified,rights_verified,device_verified,employee_approved)):
        return 'PUBLICATION_NOT_APPROVED'
    return 'ELIGIBLE_FOR_HUMAN_POSTING'
