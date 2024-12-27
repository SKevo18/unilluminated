import typing as t

import pygame

from triedy.kamera import Kamera


class Svetlo:
    def __init__(
        self,
        pozicia: t.Tuple[int, int],
        radius=150,
        intenzita=1.0,
        farba=(255, 255, 255),
    ):
        self.pozicia = pozicia
        """Pozícia svetla vo "world space"."""
        self.originalny_radius = radius
        """Pôvodný rádius svetla v pixeloch."""
        self.intenzita = intenzita
        """Intenzita svetla."""
        self.farba = farba
        """Farba svetla."""

        self._radius: float = self.originalny_radius

    def vytvor_povrch(self) -> pygame.Surface:
        """
        Vytvorí povrch pre svetlo (svetelný kruh).
        """
        # Prispôsobenie rádiusu na základe zoomu
        radius = self._radius * Kamera.PRIBLIZENIE
        povrch = pygame.Surface((radius, radius), pygame.SRCALPHA)

        for r in range(round(radius), -1, -1):
            # intenzita sa od vonka postupne znižuje
            alpha = int((1 - (r / radius)) * 255 * self.intenzita)
            # kruh po kruhu, tvoria gradient
            pygame.draw.circle(
                povrch, (*self.farba, alpha), (radius / 2, radius / 2), r
            )

        return povrch

    def aplikuj_na_tmu(self, tmavy_povrch: pygame.Surface):
        """
        Aplikuje svetlo na tmavý povrch ("vyreže tmu"),
        pričom zohľadní zoom a offset kamery pri kreslení.
        """
        # pulzovanie svetla
        self._radius -= 0.1
        if self._radius < self.originalny_radius - 10:
            self._radius = self.originalny_radius + 10

        radius = self._radius * Kamera.PRIBLIZENIE

        # world-space -> screen-space
        x_na_obrazovke = (
            self.pozicia[0] - Kamera.OFFSET.x
        ) * Kamera.PRIBLIZENIE - radius / 2
        y_na_obrazovke = (
            self.pozicia[1] - Kamera.OFFSET.y
        ) * Kamera.PRIBLIZENIE - radius / 2

        # aplikácia svetla na tmavý povrch
        tmavy_povrch.blit(self.vytvor_povrch(), (x_na_obrazovke, y_na_obrazovke))
