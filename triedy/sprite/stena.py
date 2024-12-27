import typing as t

from triedy.sprite import Sprite


class Stena(Sprite):
    def __init__(self, pozicia: t.Tuple[int, int]):
        super().__init__(pozicia)
