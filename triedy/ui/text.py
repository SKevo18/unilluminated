import typing as t

import pygame

from triedy.sprite import Sprite


class Text(Sprite):
    """
    Textový objekt.
    """

    def __init__(
        self,
        pozicia: t.Tuple[int, int],
        text: str,
        velkost_textu: int = 20,
        farba=(255, 255, 255),
        pozadie=(0, 0, 0, 0),
    ):
        self.pozadie = pozadie
        self.text_objekt = pygame.font.Font(
            self.ASSETY_ROOT / "FiraCode.ttf", velkost_textu
        ).render(text, True, farba, self.pozadie)
        super().__init__(pozicia, self.text_objekt.get_size())

    def update(self):
        self.image.fill(self.pozadie)
        self.image.blit(self.text_objekt, (0, 0))
