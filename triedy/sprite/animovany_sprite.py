"""
Modul pre triedu animovaného sprite - obsahuje sekvenciu obrázkov ktoré sa postupne menia.
"""

from pathlib import Path
import pygame

from triedy.sprite.osvetleny_sprite import OsvetlenySprite


class AnimovanySprite(OsvetlenySprite):
    """
    Predstavuje animovaný sprite.
    """

    CACHE_ANIMACII: "dict[str, list[pygame.Surface]]" = {}

    def __init__(
        self,
        animacia_id: str,
        pozicia: tuple[int, int],
        velkost: tuple[int, int],
        cesta_k_obrazkom: Path,
    ):
        super().__init__(pozicia, velkost, cesta_k_obrazkom)
        self.animacia_id = animacia_id
        self.index = 0

    @classmethod
    def nacitaj_animacie(cls, kluc: str, cesta_k_obrazkom: Path):
        """
        Načíta animácie z daného adresára pod určitým kľúčom.

        Ak už existujú animácie v cache, vráti ich.
        """

        if kluc in cls.CACHE_ANIMACII:
            return cls.CACHE_ANIMACII[kluc]

        cls.CACHE_ANIMACII[kluc] = []
        for obrazok in cesta_k_obrazkom.iterdir():
            obrazok = pygame.image.load(obrazok).convert_alpha()
            cls.CACHE_ANIMACII[kluc].append(obrazok)

        return cls.CACHE_ANIMACII[kluc]

    def update(self):
        """
        Aktualizuje a vykreslí animáciu.
        """

        self.index += 1
        self.index %= len(self.CACHE_ANIMACII[self.animacia_id])

        self.zmenit_obrazok(self.CACHE_ANIMACII[self.animacia_id][self.index])
        self._vykresli_svetlo()
