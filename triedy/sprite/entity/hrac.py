import typing as t

import pygame

from triedy.sprite.sprite import Sprite


class Hrac(Sprite):
    """
    Hlavná postava hry.
    """

    def __init__(self, pozicia: t.Tuple[int, int]):
        super().__init__(pozicia, (16, 16), "hrac.png")
        self.velocita = pygame.Vector2(0, 0)
        self.rychlost = 2

    def spracuj_event(self, event: pygame.event.Event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                self.velocita.x = -1
            elif event.key == pygame.K_RIGHT:
                self.velocita.x = 1
            elif event.key == pygame.K_UP:
                self.velocita.y = -1
            elif event.key == pygame.K_DOWN:
                self.velocita.y = 1
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                self.velocita.x = 0
            elif event.key == pygame.K_RIGHT:
                self.velocita.x = 0
            elif event.key == pygame.K_UP:
                self.velocita.y = 0
            elif event.key == pygame.K_DOWN:
                self.velocita.y = 0

    def update(self):
        if self.velocita.length() > 0:
            self.rect = self.rect.move(self.velocita.normalize() * self.rychlost)
