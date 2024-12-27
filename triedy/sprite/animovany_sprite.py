import typing as t
from pathlib import Path

import pygame

from triedy.sprite.sprite import Sprite


class AnimovanySprite(Sprite):
    """
    Predstavuje animovaný sprite.
    """

    CACHE_ANIMACII: t.Dict[str, t.List[pygame.Surface]] = {}

    def __init__(
        self,
        animacia_id: str,
        pozicia: t.Tuple[int, int],
        velkost=(16, 16),
        cesta_k_obrazkom: t.Optional[t.Union[Path, str]] = None,
    ):
        super().__init__(pozicia, velkost, cesta_k_obrazkom)
        self.animacia_id = animacia_id
        self.index = 0

    @classmethod
    def nacitaj_animacie(cls, kluc: str, cesta_k_obrazkom: t.Union[Path, str]):
        """
        Načíta animácie z daného adresára pod určitým kľúčom. Ak už existujú animácie v cache, vráti ich.

        `@classmethod` preto, aby každý potomok mal svoj vlastný cache.
        """

        if kluc in cls.CACHE_ANIMACII:
            return cls.CACHE_ANIMACII[kluc]

        cls.CACHE_ANIMACII[kluc] = []
        for obrazok in (cls.ASSETY_ROOT / cesta_k_obrazkom).iterdir():
            obrazok = pygame.image.load(obrazok).convert_alpha()
            cls.CACHE_ANIMACII[kluc].append(obrazok)

        return cls.CACHE_ANIMACII[kluc]

    def update(self):
        """
        Aktualizuje a vykreslí animáciu.
        """

        self.index += 1
        self.index %= len(self.CACHE_ANIMACII[self.animacia_id])

        self.image = self.CACHE_ANIMACII[self.animacia_id][self.index]
        super().update()
