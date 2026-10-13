GENRES=('AI・仕事効率化','美容・身だしなみ','恋愛・心理','お金・節約','営業・ビジネス','転職・キャリア','健康・生活改善','雑学・科学','旅行・グルメ','商品比較・暮らし')
STAGES=((0,.95,'SELECT'),(.95,2.05,'FORMULA'),(2.05,3,'VERIFY'))
def validate(values=(120,150,200,250),total=720,formula='=SUM(B2:B5)',genre=GENRES[0]):
    if genre not in GENRES or len(values)!=4 or any(type(x)!=int or x<0 for x in values) or sum(values)!=total or formula!='=SUM(B2:B5)': raise ValueError('invalid proof')
    return True
def stage_at(t):
    if not 0<=t<3: raise ValueError('time')
    return next(i for i,(a,b,_) in enumerate(STAGES) if a<=t<b)
def readiness(narration_language_verified=False,narration_caption_sync_verified=False,rights_approved=False,human_approved=False):
    return {'publication':'APPROVED' if all((narration_language_verified,narration_caption_sync_verified,rights_approved,human_approved)) else 'NOT_APPROVED'}
