"""
Modul pre triedu osvetleného sprite - obsahuje funkciu na zmenu úrovne svetla pre sprite.
"""

from pathlib import Path

import pygame

from triedy.sprite import Sprite


class OsvetlenySprite(Sprite):
    """
    Predstavuje sprite, ktorý je osvetlený určitou úrovňou svetla (percento).

    Predvolene je úroveň svetla 1.0 (100 %). Znižovanie hodnoty postupne stmavuje obrázok.
    """

    def __init__(
        self, pozicia: tuple[int, int], velkost: tuple[int, int], cesta_k_obrazku: Path
    ):
        super().__init__(pozicia, velkost, cesta_k_obrazku)
        self.uroven_svetla = 1.0

        self.svetlo = pygame.Surface(
            velkost,
            pygame.SRCALPHA,
        )
        self.svetlo.fill((0, 0, 0, 0))  # čierna farba (predstavuje "tmu")

        self._vykresli_svetlo()

    def zmenit_uroven_svetla(self, nova_uroven_svetla: float):
        """
        Aktualizuje úroveň svetla pre sprite a svetlo znovu vykreslí.
        """

        self.uroven_svetla = nova_uroven_svetla
        self._vykresli_svetlo()

    def _vykresli_svetlo(self):
        self.svetlo.set_alpha(
            round(255 * self.uroven_svetla)
        )  # nastavenie priehľadnosti
        self.image.blit(
            self.svetlo, (0, 0)
        )  # vloženie svetla na vrch pôvodného obrázku
