"""
Modul pre hernú slučku.
"""

from pathlib import Path
import pygame
import pygame_widgets
import pygame_widgets.button

from triedy.sprite import Sprite, OsvetlenySprite
from triedy.ui import Tlacidlo


class HernaSlucka(pygame.sprite.Group):
    """
    Hlavná herná slučka, ktorá obsahuje všetky herné objekty.
    """

    def __init__(self, cesta_k_assetom: Path):
        super().__init__()

        pygame.init()
        pygame.display.init()
        pygame.display.set_caption("test")

        self.cesta_k_assetom = cesta_k_assetom

        self.okno = pygame.display.set_mode((800, 600))
        self.clock = pygame.time.Clock()

        self.tlacidla = [
            Tlacidlo(self.okno, (100, 150), "Klikni", lambda: print("Kliknuté"))
        ]

    def spusti(self):
        test_sprite = OsvetlenySprite(
            pozicia=(0, 16 * 5),
            velkost=(16 * 5, 16 * 5),
            cesta_k_obrazku=self.cesta_k_assetom / "test.png",
        )

        self.add(
            Sprite(
                pozicia=(0, 0),
                velkost=(16 * 5, 16 * 5),
                cesta_k_obrazku=self.cesta_k_assetom / "test.png",
            ),
            test_sprite,
        )

        bezi = True
        while bezi:
            self.okno.fill((0, 0, 0))
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()

            test_sprite.uroven_svetla -= 0.01
            if test_sprite.uroven_svetla <= 0.0:
                test_sprite.uroven_svetla = 1.0

            self.update()
            self.draw(self.okno)

            pygame_widgets.update(events)
            pygame.display.flip()
            self.clock.tick(60)

        pygame.quit()
