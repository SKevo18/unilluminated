import typing as t

import pygame

from triedy.sprite.sprite import Sprite
from triedy.scena.manazer_scen import ManazerScen


class Scena(pygame.sprite.Group):
    """
    Všeobecná trieda pre scénu.
    """

    def __init__(self, *sprity: t.Union[Sprite, pygame.sprite.Group]):
        super().__init__(*sprity)

    @classmethod
    def zmen_scenu(cls, index: int):
        ManazerScen.zmen_scenu(index)

    def pred_zmenou(self):
        """
        Funkcia, ktorá sa spustí pred zmenou scény.
        """

    def pred_zmenou_na_dalsiu(self):
        """
        Funkcia, ktorá sa spustí pred zmenou na inú scénu.
        """
