import typing as t
from pathlib import Path

import pygame

from triedy.sprite import Sprite


class Tlacidlo(Sprite):
    """
    Tlačidlo, na ktoré sa dá kliknúť.
    """

    def __init__(
        self,
        pozicia: t.Tuple[int, int],
        text: str,
        po_kliknuti: t.Callable[[], None],
        velkost = (200, 100),
        velkost_textu: t.Optional[int] = None,
    ):
        super().__init__(pozicia, velkost, Path("ui") / "tlacidlo.png")
        self.po_kliknuti = po_kliknuti
        self.velkost_textu = velkost_textu if velkost_textu else self.velkost[1] // 4

        self.kliknute = False
        self.obrazok_original = self.image.copy()
        self.obrazok_kliknute = self.nacitaj_obrazok(Path("ui") / "tlacidlo_klik.png")
        self.obrazok_hover = self.nacitaj_obrazok(Path("ui") / "tlacidlo_hover.png")
        self.text = pygame.font.Font(
            self.ASSETY_ROOT / "FiraCode.ttf", self.velkost_textu
        ).render(text, False, (0, 0, 0))

    def update(self):
        # na tlačidlo ešte vypíšeme text tlačidla:
        img_rect = self.image.get_rect()
        self.image.blit(
            self.text,
            (
                img_rect.centerx - (self.text.get_width() // 2),
                img_rect.centery - (self.text.get_height() // 2),
            ),
        )

    def spracuj_event(self, event: pygame.event.Event, _):
        if event.type == pygame.MOUSEBUTTONDOWN:  # začneme klikať a držíme myš
            if self.rect.collidepoint(event.pos):
                self.kliknute = True
                self.image = self.obrazok_kliknute
        elif event.type == pygame.MOUSEBUTTONUP and self.kliknute:  # pustíme myš
            self.kliknute = False
            self.image = self.obrazok_original

            if self.rect.collidepoint(event.pos):  # ak sme si to nerozmysleli
                self.po_kliknuti()
        elif event.type == pygame.MOUSEMOTION:  # pohyb myši
            if self.kliknute:
                return

            if self.rect.collidepoint(event.pos):  # pohybujeme sa v rámci tlačidla
                self.image = self.obrazok_hover
            else:
                # tuto je nevýhoda že sa to nastavuje za každým pohybom myši mimo tlačidla
                # ...ale nie je čas vymýšľať sofistikovanejšiu logiku:
                self.image = self.obrazok_original
