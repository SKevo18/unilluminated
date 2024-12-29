import typing as t
from pathlib import Path

import pygame
from pygame.event import Event

from triedy.mixer import Mixer
from triedy.sprity.sprite import Sprite
from triedy.ui.text import Text


class ZaskrtavaciePole(pygame.sprite.Group):
    """
    Zaškrtávacie pole, obsahuje interaktívny box a text (štítok).
    """

    def __init__(
        self,
        pozicia: t.Tuple[int, int],
        radius: int,
        text: str,
        po_kliknuti: t.Callable[[bool], None],
        zaskrtnute: bool = False,
    ):
        self.box = ZaskrtavaciePoleBox(pozicia, radius, po_kliknuti, zaskrtnute)
        self.text = Text(
            (
                self.box.rect.right + radius // 2,
                (self.box.rect.centery - radius // 2) - 6,
            ),
            text,
            velkost_textu=radius,
            farba=(255, 255, 255),
        )
        super().__init__(self.text, self.box)


class ZaskrtavaciePoleBox(Sprite):
    """
    Box zaškrtávacieho poľa.
    """

    def __init__(
        self,
        pozicia: t.Tuple[int, int],
        radius: int,
        po_kliknuti: t.Callable[[bool], None],
        zaskrtnute: bool = False,
    ):
        super().__init__(
            pozicia, (radius * 2, radius * 2), Path("ui") / "zaskrtavacie_pole.png"
        )
        self.po_kliknuti = po_kliknuti
        self.je_zaskrtnute = zaskrtnute

        self.bez_fajky = self.image.copy()
        self.fajka = self.nacitaj_obrazok(Path("ui") / "zaskrtavacie_pole_fajka.png")

    def update(self):
        self.image = self.bez_fajky.copy()

        if self.je_zaskrtnute:
            self.image.blit(self.fajka, (0, 0))

    def prepni(self):
        self.je_zaskrtnute = not self.je_zaskrtnute
        self.po_kliknuti(self.je_zaskrtnute)
        Mixer.prehrat_zvuk("poloz")

    def spracuj_event(self, event: Event, _):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.prepni()
