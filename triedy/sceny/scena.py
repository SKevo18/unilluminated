import typing as t

import pygame

from triedy.sceny.manazer_scen import ManazerScen
from triedy.sprity.sprite import Sprite


class Scena(pygame.sprite.Group):
    """
    Všeobecná trieda pre scénu.
    """

    def __init__(self, *sprity: t.Union[Sprite, pygame.sprite.Group]):
        super().__init__(*sprity)
        self.velkost_spritu = 16
        """Veľkosť jedného sprite v pixeloch, predvolene 16."""

        self.ui_elementy = pygame.sprite.Group()
        """Skupina UI elementov."""

    @staticmethod
    def zmen_scenu(index: int):
        ManazerScen.zmen_scenu(index)
    

    @staticmethod
    def aktualny_index_sceny():
        return ManazerScen.index_aktualnej_sceny

    def pred_zmenou(self):
        """
        Funkcia, ktorá sa spustí pred zmenou scény.
        """
        pass

    def pred_zmenou_na_dalsiu(self):
        """
        Funkcia, ktorá sa spustí pred zmenou na inú scénu.
        """
        pass

    def update(self):
        self._update_rekurzia(self)

    def _update_rekurzia(self, skupina: pygame.sprite.Group):
        """
        Pomocná funkcia pre rekurzívne aktualizovanie spritov v skupine.
        """

        for sprite in skupina.sprites():
            sprite.update()
            if isinstance(sprite, pygame.sprite.Group):
                # vnorená skupina, aktualizujeme rekurzívne
                self._update_rekurzia(sprite)
