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
        """Pôvodný rádius svetla v pixeloch (používa sa pre animáciu pulzovania)."""
        self.intenzita = intenzita
        """Intenzita svetla."""
        self.farba = farba
        """Farba svetla."""
        self.zapnute = True
        """Ak je `True`, emituje svetlo."""

        self._radius: float = self.originalny_radius
        """Aktuálny radius svetla v pixeloch."""
        self._pulzuje_naspat = False
        """Ak je `True`, svetlo v aktuálnej fáze animácie pulzuje naspäť."""

    def vytvor_povrch(self) -> pygame.Surface:
        """
        Vytvorí povrch pre svetlo (svetelný kruh).
        """
        # prispôsobiť radius zoomu
        radius = round(self._radius * Kamera.PRIBLIZENIE)
        povrch = pygame.Surface((radius * 2, radius * 2), pygame.SRCALPHA)

        # 20 segmentov v gradiente (ak ich je veľa, hra seká)
        krok = max(1, radius // 20)
        for r in range(radius, -1, -krok):
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
        # iba zapnuté svetlo svieti
        if not self.zapnute:
            return

        # pulzovanie svetla = zmena radiusu +- 1
        self._radius += -0.1 if self._pulzuje_naspat else 0.1
        if (
            self._radius < self.originalny_radius - 5
            or self._radius > self.originalny_radius + 5
        ):
            self._pulzuje_naspat = not self._pulzuje_naspat

        # aplikácia svetla na tmavý povrch
        radius = round(self._radius * Kamera.PRIBLIZENIE)
        stred_obrazovky = (
            pygame.Vector2(tmavy_povrch.get_size()) / 2  # referencny bod v screen-space
        )

        # podobné ako v `Kamera.aplikuj_na_sprite`
        # (ale keďže svetlo nie je sprite, musíme to urobiť ručne):
        pozicia_pred_zoomom = pygame.Vector2(self.pozicia) - Kamera.OFFSET
        pozicia_po_zoome = (
            pozicia_pred_zoomom - stred_obrazovky
        ) * Kamera.PRIBLIZENIE + stred_obrazovky  # pozícia v screen-space

        # "výrez" do tmy
        tmavy_povrch.blit(
            self.vytvor_povrch(),
            (
                pozicia_po_zoome.x - radius,
                pozicia_po_zoome.y - radius,
            ),
        )
