from rail import overlay
from guard import GENRES
assert len(GENRES) == 10
assert overlay([{'start': 0}, {'start': 1}, {'start': 2}]).count('drawbox=') == 6
print('rail checks passed')
