"""Technical quality invariants for cycle510 preview."""
WIDTH = 1080
HEIGHT = 1920
MIN_SECONDS = 15
MAX_SECONDS = 25
GENRE_COUNT = 10
VOICE_REQUIRED_FOR_PUBLICATION = True
EMPLOYEE_APPROVAL_REQUIRED = True

def valid_video(width, height, seconds):
    return width == WIDTH and height == HEIGHT and MIN_SECONDS <= seconds <= MAX_SECONDS
