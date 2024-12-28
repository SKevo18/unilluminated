import typing as t
from pathlib import Path

import pygame

from triedy.kamera import Kamera
from triedy.sprite.sprite import Sprite


class AnimovanySprite(Sprite):
    """
    Predstavuje animovaný sprite.
    """

    CACHE_ANIMACII: t.Dict[str, t.List[pygame.Surface]] = {}

    def __init__(
        self,
        pozicia: t.Tuple[int, int],
        velkost=(16, 16),
        animacia_id: t.Optional[str] = None,
        cesta_k_obrazkom: t.Optional[t.Union[Path, str]] = None,
    ):
        super().__init__(pozicia, velkost, None)
        self.animacia_id = animacia_id
        """ID animácií. Ak je `None`, tak sa neanimuje."""
        self.cas_animacie = 0
        """Čas animácie v milisekundách."""

        self.animuj = True
        """Ak je `True`, obrázky sa menia v metóde `update()`."""

        # ak neexistujú obrázky, nevykreslí sa nič:
        if self.animacia_id is not None and cesta_k_obrazkom is not None:
            self.nacitaj_animacie(self.animacia_id, cesta_k_obrazkom)

    def nacitaj_animacie(
        self,
        kluc: str,
        cesta_k_obrazkom: t.Optional[t.Union[Path, str]] = None,
    ):
        """
        Načíta animácie z daného adresára pod určitým kľúčom.
        Ak už existujú animácie v cache (alebo `cesta_k_obrazkom` je `None`), vráti ich.

        `@classmethod` preto, aby každý potomok mal svoj vlastný cache.
        """

        if cesta_k_obrazkom is None or kluc in self.CACHE_ANIMACII:
            return self.CACHE_ANIMACII[kluc]

        self.CACHE_ANIMACII[kluc] = []
        for obrazok in (self.ASSETY_ROOT / cesta_k_obrazkom).iterdir():
            obrazok = pygame.image.load(obrazok).convert_alpha()
            self.CACHE_ANIMACII[kluc].append(obrazok)

        return self.CACHE_ANIMACII[kluc]

    @property
    def animacie(self):
        if self.animacia_id is None:
            return []

        return self.nacitaj_animacie(self.animacia_id)

    def update(self):
        if self.animacia_id is None:
            return super().update()

        if self.animuj:
            self.cas_animacie += 1

        obrazok = self.animacie[self.cas_animacie // 10 % len(self.animacie)]
        if self.je_otoceny:
            obrazok = pygame.transform.flip(obrazok, True, False)

        self.image = obrazok
        return super().update()
