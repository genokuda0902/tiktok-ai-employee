GENRES = ('ai_work', 'beauty', 'relationship', 'money', 'sales', 'career', 'health', 'science', 'travel', 'products')
SAFE_ZONE = (72, 1450, 1008, 1724)

def validate_caption(text):
    if not isinstance(text, str) or not 1 <= len(text) <= 17 or '\n' in text:
        raise ValueError('caption length')
    return True
