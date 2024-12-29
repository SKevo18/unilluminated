import typing as t

import pygame

import nastavenia as n
from triedy.sprity.entity.prisera import Prisera


class PriamociaraPrisera(Prisera):
    """
    Príšera, ktorá sa pohybuje priamo smerom k hráčovi.
    """

    ciel: t.Optional[t.Tuple[int, int]] = None
    """Pozícia, ku ktorej sa všetky príšery snažia dostať."""

    def __init__(self, pozicia: t.Tuple[int, int]):
        super().__init__(
            pozicia,
            n.ASSETY_ROOT / "sprite" / "prisera",
            radius_svetla=3,
            rozsah_pulzovania=5,
            intenzita_svetla=1.0,
            farba_svetla=(255, 0, 0),
            rychlost=0.3,
        )

    def update(self):
        if self.ciel:
            # smer pohybu
            smer = pygame.Vector2(self.ciel) - pygame.Vector2(self.rect.center)
            if smer.length() > 0:
                self.velocita = smer.normalize() * self.rychlost
                self.je_otoceny = self.velocita.x > 0
            else:
                self.velocita = pygame.Vector2(0, 0)
        return super().update()
