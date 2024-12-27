import typing as t

import pygame

from triedy.kamera import Kamera


class Svetlo:
    def __init__(
        self,
        pozicia: t.Tuple[int, int],
        radius=80,
        intenzita=1.0,
        farba=(255, 255, 255),
    ):
        self.pozicia = pozicia
        self.radius = radius
        """Rádius svetla v pixeloch."""
        self.intenzita = intenzita
        """Intenzita svetla."""
        self.farba = farba
        """Farba svetla."""

        self.povrch = self.vytvor_povrch()

    def vytvor_povrch(self) -> pygame.Surface:
        """
        Vytvorí povrch pre svetlo (svetelný kruh).
        """
        povrch = pygame.Surface((self.radius * 2, self.radius * 2), pygame.SRCALPHA)
        stred = (self.radius, self.radius)

        for r in range(self.radius, -1, -1):
            alpha = int((1 - (r / self.radius)) * 255 * self.intenzita)
            pygame.draw.circle(povrch, (*self.farba, alpha), stred, r)

        return povrch

    def aplikuj_na_tmu(self, tmavy_povrch: pygame.Surface):
        """
        Aplikuje svetlo na tmavý povrch ("vyreže tmu").
        """
        pozicia_pred_zoomom = pygame.Vector2(self.pozicia) - Kamera.OFFSET
        stred_obrazovky = pygame.Vector2(tmavy_povrch.get_size()) / 2
        pozicia_po_zoome = (
            pozicia_pred_zoomom - stred_obrazovky
        ) * Kamera.PRIBLIZENIE + stred_obrazovky

        pozicia = (pozicia_po_zoome.x - self.radius, pozicia_po_zoome.y - self.radius)
        tmavy_povrch.blit(self.povrch, pozicia)
