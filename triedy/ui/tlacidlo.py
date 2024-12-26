import typing as t
from pathlib import Path

import pygame

from triedy.sprite import Sprite


class Tlacidlo(Sprite):
    def __init__(self, pozicia: tuple[int, int], text: str, po_kliknuti: t.Callable):
        super().__init__(pozicia, (300, 150), Path("ui") / "tlacidlo.png")
        self.text = text
        self.po_kliknuti = po_kliknuti

        self.kliknute = False
        self.obrazok_original = self.image.copy()
        self.obrazok_kliknute = self.nacitaj_obrazok(Path("ui") / "tlacidlo_klik.png")
        self.obrazok_hover = self.nacitaj_obrazok(Path("ui") / "tlacidlo_hover.png")

    def update(self):
        super().update()
        self.image.blit(
            pygame.font.Font(None, 50).render(self.text, True, (0, 0, 0)), (10, 10)
        )

    def spracuj_event(self, event: pygame.event.Event):
        if event.type == pygame.MOUSEBUTTONDOWN:  # začneme klikať a držíme myš
            if self.rect.collidepoint(event.pos):
                self.kliknute = True
                self.image = self.obrazok_kliknute
        elif event.type == pygame.MOUSEBUTTONUP:  # klikneme a pustíme myš
            if self.kliknute:
                self.kliknute = False
                self.image = self.obrazok_original

                if self.rect.collidepoint(event.pos):  # ak sme si to nerozmysleli
                    self.po_kliknuti()
        elif event.type == pygame.MOUSEMOTION:
            if self.kliknute:
                return

            if self.rect.collidepoint(event.pos):
                self.image = self.obrazok_hover
            else:
                self.image = self.obrazok_original
