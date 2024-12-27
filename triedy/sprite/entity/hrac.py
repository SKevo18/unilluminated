import typing as t

import pygame

from triedy.sprite.entity.svetelna_entita import SvetelnaEntita
from triedy.kamera import Kamera


class Hrac(SvetelnaEntita):
    """
    Hlavná postava hry.
    """

    def __init__(self, pozicia: t.Tuple[int, int]):
        super().__init__(pozicia, (16, 16), "hrac.png", rychlost=0.5)

    def spracuj_event(self, event: pygame.event.Event):
        if event.type == pygame.KEYDOWN:
            # pohyb
            if event.key == pygame.K_LEFT:
                self.velocita.x = -1
            elif event.key == pygame.K_RIGHT:
                self.velocita.x = 1
            elif event.key == pygame.K_UP:
                self.velocita.y = -1
            elif event.key == pygame.K_DOWN:
                self.velocita.y = 1

            # približovanie kamery
            elif event.key == pygame.K_p:
                Kamera.zmen_priblizenie(0.5)
            elif event.key == pygame.K_o:
                Kamera.zmen_priblizenie(-0.5)
        elif event.type == pygame.KEYUP:
            # pohyb
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
