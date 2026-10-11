from quality_cycle496 import manifest_for
from render_cycle496 import SCENES, DATA
assert manifest_for(SCENES, DATA)['evidence_total'] == 720
