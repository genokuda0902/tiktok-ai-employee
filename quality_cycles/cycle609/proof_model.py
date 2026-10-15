"""Shared data checks for evidence-led short videos (10 genres)."""
from dataclasses import dataclass

GENRES = (
    "AI仕事効率化", "恋愛", "美容", "お金", "雑学",
    "ガジェット", "筋トレ", "営業", "旅行", "ミステリー"
)

@dataclass(frozen=True)
class Proof:
    labels: tuple[str, ...]
    values: tuple[int, ...]

    def validate(self):
        if not 2 <= len(self.values) <= 8 or len(self.labels) != len(self.values):
            raise ValueError("Invalid evidence dimensions")
        if any(not isinstance(v, int) or v < 0 for v in self.values):
            raise ValueError("Invalid evidence values")
        if max(self.values) == 0:
            raise ValueError("All-zero evidence")

    @property
    def total(self):
        self.validate()
        return sum(self.values)

    @property
    def peak(self):
        self.validate()
        return self.labels[self.values.index(max(self.values))]

SAMPLE = Proof(("1月","2月","3月","4月"),(120,150,200,250))
