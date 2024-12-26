import typing as t
from pathlib import Path

import pygame

from triedy.sprite import Sprite


class Tlacidlo(Sprite):
    def __init__(self, pozicia: tuple[int, int], text: str, po_kliknuti: t.Callable):
        super().__init__(pozicia, (300, 150), Path("ui") / "tlacidlo.png")
        self.text = text
        self.po_kliknuti = po_kliknuti

    def update(self):
        super().update()
        self.image.blit(
            pygame.font.Font(None, 50).render(self.text, True, (0, 0, 0)), (10, 10)
        )
