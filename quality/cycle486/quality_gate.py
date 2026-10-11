"""Review-only safety check for TikTok video scenes."""

def allow_review(publication_status):
    return publication_status == 'NOT_APPROVED'
