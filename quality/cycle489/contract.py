"""Cycle489 reusable, review-only evidence validation."""
VALUES=(120,150,200,250)
GENRES=('ai_productivity','trivia','miniature','before_after','product_comparison','food','education','story','life_hacks','science')
def validate(values=VALUES, genre='ai_productivity', rights='SYNTHETIC_LOCAL', publication='NOT_APPROVED', auto_post=False):
    if genre not in GENRES: raise ValueError('unknown genre')
    if len(values)!=4 or any(type(x)!=int or x<0 for x in values): raise ValueError('invalid source data')
    if sum(values)!=720: raise ValueError('source and displayed total differ')
    if rights!='SYNTHETIC_LOCAL' or publication!='NOT_APPROVED' or auto_post: raise ValueError('human review required')
    return True
