from dataclasses import dataclass


@dataclass(frozen=True)
class NativeStoryCardContract:
    width: int = 1080
    height: int = 1920
    min_cards: int = 6
    max_cards: int = 12
    human_approval_required: bool = True
    manual_post_only: bool = True
    zero_cost: bool = True

    def validate(self, card_count: int, rights_approved: bool) -> None:
        if (self.width, self.height) != (1080, 1920):
            raise ValueError("native story cards must be 1080x1920")
        if not self.min_cards <= card_count <= self.max_cards:
            raise ValueError("story must contain 6-12 native vertical cards")
        if not rights_approved:
            raise ValueError("all card assets must be rights-approved")


def default_story_beats():
    return ("hook", "before", "prompt", "process", "result", "before_after", "extensions", "cta")
