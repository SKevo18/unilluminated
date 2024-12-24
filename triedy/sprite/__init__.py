"""
Modul pre triedu sprite - predstavuje klasický obrázok, bez animácií.
"""

from pathlib import Path
import pygame


class Sprite(pygame.sprite.Sprite):
    """
    Predstavuje klasický obrázok, bez animácií.
    """

    def __init__(
        self, pozicia: tuple[int, int], velkost: tuple[int, int], cesta_k_obrazku: Path
    ):
        super().__init__()
        self.image = pygame.image.load(cesta_k_obrazku).convert_alpha()
        self.image = pygame.transform.scale(self.image, velkost)

        self.rect = self.image.get_rect()
        self.rect.x = pozicia[0]
        self.rect.y = pozicia[1]

    def zmenit_obrazok(self, novy_obrazok: pygame.Surface):
        """
        Setter pre obrázok spritu.
        """

        self.image = novy_obrazok
