import typing as t

from random import choice
import pygame

from triedy.sprite.entity.entita import Entita


class OdrazajucaPrisera(Entita):
    """
    Príšera, ktorá sa odráža od stien.
    """

    def __init__(self, pozicia: t.Tuple[int, int]):
        super().__init__(
            pozicia,
            self.ASSETY_ROOT / "sprite" / "prisera",
            rychlost=0.5,
        )

        self.velocita = pygame.Vector2(choice([-1, 1]), choice([-1, 1]))

    def pohyb(self, solidna_maska: pygame.mask.Mask):
        # to isté ako v `Entita.pohyb`, iba meníme smer ak narazí
        if not self.moze_ist:
            return

        # pohyb po X osi
        nove_x = self.pozicia.x + self.velocita.x
        maska_pozicia = (nove_x, self.rect.y + self.maska_offset[1])
        if not solidna_maska.overlap(self.maska, maska_pozicia):
            self.pozicia.x = nove_x
        else:
            self.velocita.x = -self.velocita.x

        # pohyb po Y osi
        nove_y = self.pozicia.y + self.velocita.y
        maska_pozicia = (self.pozicia.x, nove_y + self.maska_offset[1])
        if not solidna_maska.overlap(self.maska, maska_pozicia):
            self.pozicia.y = nove_y
        else:
            self.velocita.y = -self.velocita.y

        self.velocita = self.velocita.normalize() * self.rychlost
        self.rect.topleft = self.pozicia
