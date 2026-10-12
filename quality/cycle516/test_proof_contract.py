from quality.cycle516.proof_contract import validate

def test_total():
    m = {'genre':'ai_work','rights':'synthetic_local_review_only','privacy_checked':True,'publication':'NOT_APPROVED','human_review':'HUMAN_REVIEW','auto_post':False,'values':[120,150,200,250]}
    assert validate(m) == 720
