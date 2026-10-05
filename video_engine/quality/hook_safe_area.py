"""Fail-closed hook safe-area validation."""
SAFE_LEFT, SAFE_RIGHT, SAFE_TOP, SAFE_BOTTOM = 60, 900, 180, 1600

def validate_hook_safe_area(elements):
    if not isinstance(elements, list) or not elements:
        return False, ["hook_elements_missing"]
    errors = []
    for index, element in enumerate(elements):
        if not isinstance(element, dict):
            errors.append(f"element_{index}_invalid"); continue
        if not element.get("important", True):
            continue
        box = element.get("box")
        if not isinstance(box, (list, tuple)) or len(box) != 4:
            errors.append(f"element_{index}_box_invalid"); continue
        try:
            x, y, w, h = map(float, box)
        except (TypeError, ValueError):
            errors.append(f"element_{index}_box_invalid"); continue
        if w <= 0 or h <= 0:
            errors.append(f"element_{index}_box_invalid"); continue
        if x < SAFE_LEFT or y < SAFE_TOP or x + w > SAFE_RIGHT or y + h > SAFE_BOTTOM:
            errors.append(f"element_{index}_outside_safe_area")
    return not errors, errors
