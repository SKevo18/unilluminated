import typing as t

from triedy.sprity.sprite import Sprite


class Podlaha(Sprite):
    def __init__(self, pozicia: t.Tuple[int, int]):
        super().__init__(pozicia)
