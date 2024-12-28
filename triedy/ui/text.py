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
        self._text = text
        self.velkost_textu = velkost_textu
        self.farba = farba
        self.pozadie = pozadie

        self.text_objekt = pygame.font.Font(
            self.ASSETY_ROOT / "FiraCode.ttf", velkost_textu
        ).render(text, True, farba, self.pozadie)
        super().__init__(pozicia, self.text_objekt.get_size())

    def update(self):
        self.image.fill(self.pozadie)
        self.image.blit(self.text_objekt, (0, 0))

    @property
    def text(self):
        return self._text

    @text.setter
    def text(self, value):
        """
        Text - ak sa zmení, prekreslíme textový objekt.
        """

        self._text = value
        self.text_objekt = pygame.font.Font(
            self.ASSETY_ROOT / "FiraCode.ttf", self.velkost_textu
        ).render(self._text, True, self.farba, self.pozadie)
