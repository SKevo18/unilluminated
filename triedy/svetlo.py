import typing as t
import pygame

from triedy.kamera import Kamera


class Svetlo:
    """
    Svetlo, ktoré osvetľuje okolie.
    """

    def __init__(
        self,
        pozicia: t.Tuple[int, int],
        radius=80,
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
        self.ide_spat = False

    def vytvor_povrch(self) -> pygame.Surface:
        """
        Vytvorí povrch pre svetlo (svetelný kruh).
        """
        # prispôsobiť radius zoomu
        radius = round(self._radius * Kamera.PRIBLIZENIE)
        povrch = pygame.Surface((radius * 2, radius * 2), pygame.SRCALPHA)

        for r in range(radius, -1, -1):
            # intenzita sa od vonka postupne znižuje
            alpha = int((1 - (r / radius)) * 255 * self.intenzita)
            # kruh na kruhu, tvoria gradient
            pygame.draw.circle(povrch, (*self.farba, alpha), (radius, radius), r)

        return povrch

    def aplikuj_na_tmu(self, tmavy_povrch: pygame.Surface):
        """
        Aplikuje svetlo na tmavý povrch ("vyreže tmu"),
        pričom zohľadní zoom a offset kamery pri kreslení.
        """
        # pulzovanie svetla
        self._radius += -0.05 if self.ide_spat else 0.05
        if (
            self._radius < self.originalny_radius - 1
            or self._radius > self.originalny_radius + 1
        ):
            self.ide_spat = not self.ide_spat

        # aplikácia svetla na tmavý povrch
        radius = round(self._radius * Kamera.PRIBLIZENIE)
        tmavy_povrch.blit(
            self.vytvor_povrch(),
            (
                self.pozicia[0] - self.originalny_radius,
                self.pozicia[1] - radius,
            ),
        )
