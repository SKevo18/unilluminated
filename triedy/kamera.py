"""
Modul pre kameru.
"""

import typing as t

if t.TYPE_CHECKING:
    from triedy.sprite.entity.entita import Entita

import pygame

import nastavenia as n


class Kamera:
    """
    Kamera, ktorá sleduje hráča a posúva všetky objekty na obrazovke.
    Používa sa staticky (nie je potrebné vytvárať viac ako jednu inštanciu).
    """

    PRIBLIZENIE = 2
    """Zoom kamery."""
    OFFSET = pygame.Vector2(0, 0)
    """Aktuálny posun kamery."""

    @staticmethod
    def sleduj_entitu(entita: "Entita"):
        """
        Nastaví pozíciu kamery na pozíciu entity.
        """
        Kamera.OFFSET.x = entita.rect.centerx - n.VELKOST_OKNA[0] // 2
        Kamera.OFFSET.y = entita.rect.centery - n.VELKOST_OKNA[1] // 2

    @staticmethod
    def zmen_priblizenie(relativna_hodnota_priblizenia: float):
        """
        Priblíži alebo oddiali kameru.
        """
        Kamera.PRIBLIZENIE = min(
            5, max(1, Kamera.PRIBLIZENIE + relativna_hodnota_priblizenia)
        )

    @staticmethod
    def aplikuj_na_sprite(sprite: pygame.sprite.Sprite) -> pygame.Rect:
        """
        Aplikuje posun a priblíženie kamery na daný sprite a vráti jeho nový rect.
        Jedná sa o akýkoľvek sprite v leveli (nevzťahuje sa iba na hráča).
        """
        if sprite.rect is None:
            return pygame.Rect(0, 0, 0, 0)

        # poloha kamery, tak aby bola na stred obrazovky
        stred_obrazovky = pygame.Vector2(n.VELKOST_OKNA) / 2
        pozicia_pred_zoomom = pygame.Vector2(sprite.rect.topleft) - Kamera.OFFSET
        pozicia_po_zoome = (
            pozicia_pred_zoomom - stred_obrazovky
        ) * Kamera.PRIBLIZENIE + stred_obrazovky

        # priblizenie obrazkov spritov
        if sprite.image is not None:
            # musíme zachovať originálny obrázok:
            # v opačnom prípade sa pri približovaní počas hry nebude zobrazovať správne
            # (bude sa pixelizovať, pretože budeme exponenciálne meniť jeho veľkosť,
            # t. j. budeme približovať priblížený obrázok)
            if not hasattr(sprite, "originalny_obrazok"):
                setattr(sprite, "originalny_obrazok", sprite.image)

            sprite.image = pygame.transform.scale(
                getattr(sprite, "originalny_obrazok"),
                (
                    int(sprite.rect.width * Kamera.PRIBLIZENIE),
                    int(sprite.rect.height * Kamera.PRIBLIZENIE),
                ),
            )

        return pygame.Rect(
            pozicia_po_zoome.x,
            pozicia_po_zoome.y,
            sprite.rect.width * Kamera.PRIBLIZENIE,
            sprite.rect.height * Kamera.PRIBLIZENIE,
        )
