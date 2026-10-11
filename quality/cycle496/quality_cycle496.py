"""Cycle 496 common genre and scene contract."""
GENRES=('AI・仕事効率化','美容・身だしなみ','恋愛・心理','お金・節約','営業・ビジネス','転職・キャリア','健康・生活改善','雑学・科学','旅行・グルメ','商品比較・暮らし')
ROLES=('hook','pain','solution','prompt','formula','chart','compare','cta')

def manifest_for(scenes,data,genre='AI・仕事効率化'):
    m={'genre':genre,'supported_genres':list(GENRES),'scene_roles':[s[0] for s in scenes],'scene_frames':[round(s[3]*30) for s in scenes],'evidence_data':list(data),'evidence_total':sum(data),'progressive_evidence_frames':{'formula':[25,25,25],'chart':[15,15,15,30]},'asset_rights':'ORIGINAL_PROCEDURAL','voice_status':'SFX_ONLY_NO_JAPANESE_NARRATION','captions':'SCENE_DESCRIPTIONS_NOT_TRANSCRIPTS','human_review':'PENDING','publication':'NOT_APPROVED','automatic_posting':False}
    validate_manifest(m)
    return m
