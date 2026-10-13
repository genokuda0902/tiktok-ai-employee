"""Review-only evidence math, shared by all genres."""
GENRES = ('ai_work', 'beauty', 'relationships', 'finance', 'sales_business', 'career', 'health_lifestyle', 'science_trivia', 'travel_food', 'shopping_lifestyle')

def check_total(values, total):
    if len(values) != 4 or any(type(v) is not int or v < 0 for v in values):
        return False
    return sum(values) == total
