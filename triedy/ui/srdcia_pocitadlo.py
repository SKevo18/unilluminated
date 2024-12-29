import typing as t
from pathlib import Path

import pygame

from triedy.sprity.sprite import Sprite


class SrdciaPocitadlo(pygame.sprite.Group):
    """
    Počítadlo sŕdc zobrazené ako rad obrázkov.
    """

    def __init__(self, pozicia: t.Tuple[int, int], pocet_srdc=2):
        self.pozicia = pozicia
        self._pocet_srdc = pocet_srdc

        self.velkost = (16, 16)
        self.srdcia = self._vytvor_srdcia()
        super().__init__(self.srdcia)

    def _vytvor_srdcia(self):
        srdcia = []
        for i in range(self._pocet_srdc):
            srdce = Sprite(
                (self.pozicia[0] + i * (self.velkost[0] + 5), self.pozicia[1]),
                self.velkost,
                Path("ui") / "srdce.png",
            )
            srdcia.append(srdce)
        return srdcia

    @property
    def pocet_srdc(self) -> int:
        """
        Počet sŕdc (životov hráča)
        """

        return self._pocet_srdc

    @pocet_srdc.setter
    def pocet_srdc(self, novy_pocet: int):
        """
        Setter pre počet sŕdc, ktorý znovu vykreslí srdcia po zmene.
        """

        self._pocet_srdc = novy_pocet
        self.srdcia = self._vytvor_srdcia()
