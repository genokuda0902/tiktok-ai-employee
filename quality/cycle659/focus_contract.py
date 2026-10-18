"""Focus marker placement and release gate for a vertical video."""

ANCHORS = ((538, 755), (438, 748), (550, 800), (727, 706),
           (760, 740), (540, 738), (725, 747), (667, 723))


def validate_anchors(anchors=ANCHORS):
    if len(anchors) != 8:
        raise ValueError('expected eight scenes')
    return all(180 <= x <= 900 and 400 <= y <= 1000 for x, y in anchors)


def can_publish(rights_approved=False, employee_approved=False, audio_checked=False):
    return rights_approved and employee_approved and audio_checked
