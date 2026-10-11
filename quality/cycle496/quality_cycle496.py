"""Cycle 496 common genre and scene contract."""
GENRES=('AI・仕事効率化','美容・身だしなみ','恋愛・心理','お金・節約','営業・ビジネス','転職・キャリア','健康・生活改善','雑学・科学','旅行・グルメ','商品比較・暮らし')
ROLES=('hook','pain','solution','prompt','formula','chart','compare','cta')

def manifest_for(scenes,data,genre='AI・仕事効率化'):
    m={'genre':genre,'supported_genres':list(GENRES),'scene_roles':[s[0] for s in scenes],'scene_frames':[round(s[3]*30) for s in scenes],'evidence_data':list(data),'evidence_total':sum(data),'progressive_evidence_frames':{'formula':[25,25,25],'chart':[15,15,15,30]},'asset_rights':'ORIGINAL_PROCEDURAL','voice_status':'SFX_ONLY_NO_JAPANESE_NARRATION','captions':'SCENE_DESCRIPTIONS_NOT_TRANSCRIPTS','human_review':'PENDING','publication':'NOT_APPROVED','automatic_posting':False}
    validate_manifest(m)
    return m

def validate_manifest(m):
    if m['genre'] not in GENRES: raise ValueError('genre')
    if m['scene_roles']!=list(ROLES): raise ValueError('roles')
    if len(m['scene_frames'])!=8 or sum(m['scene_frames'])!=600: raise ValueError('duration')
    if sum(m['progressive_evidence_frames']['formula'])!=75: raise ValueError('formula')
    if sum(m['progressive_evidence_frames']['chart'])!=75: raise ValueError('chart')
    if len(m['evidence_data'])!=4: raise ValueError('data')
    if sum(m['evidence_data'])!=m['evidence_total']: raise ValueError('math')
    if m['asset_rights']!='ORIGINAL_PROCEDURAL': raise ValueError('rights')
    if m['automatic_posting'] is not False: raise ValueError('posting')
    if m['publication']!='NOT_APPROVED': raise ValueError('publication')
    return True
