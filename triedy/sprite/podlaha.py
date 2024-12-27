import typing as t

from triedy.sprite.sprite import Sprite


class Podlaha(Sprite):
    def __init__(self, pozicia: t.Tuple[int, int]):
        super().__init__(pozicia)
