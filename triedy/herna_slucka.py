"""
Modul pre hernú slučku.
"""

from pathlib import Path
import pygame

from triedy.sprite import OsvetlenySprite


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

        self.screen = pygame.display.set_mode((800, 600))
        self.clock = pygame.time.Clock()

    def spusti(self):
        test_sprite = OsvetlenySprite(
            pozicia=(0, 16 * 5),
            velkost=(16 * 5, 16 * 5),
            cesta_k_obrazku=self.cesta_k_assetom / "test.png",
        )

        self.add(
            OsvetlenySprite(
                pozicia=(0, 0),
                velkost=(16 * 5, 16 * 5),
                cesta_k_obrazku=self.cesta_k_assetom / "test.png",
            ),
            test_sprite,
        )

        bezi = True
        while bezi:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    bezi = False

            self.screen.fill("black")

            test_sprite.uroven_svetla -= 0.1
            if test_sprite.uroven_svetla <= 0.0:
                test_sprite.uroven_svetla = 1.0

            self.update()
            self.draw(self.screen)

            pygame.display.flip()
            self.clock.tick(60)

        pygame.quit()
