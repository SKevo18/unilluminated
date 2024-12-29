"""
Modul pre hernú slučku.
"""

import typing as t

import pygame

import nastavenia as n
from triedy.mixer import Mixer
from triedy.sceny.manazer_scen import ManazerScen
from triedy.sceny.levely.level import Level
from triedy.sceny.hlavne_menu import HlavneMenu
from triedy.sceny.nastavenia import Nastavenia
from triedy.sceny.koniec_hry import KoniecHry
from triedy.sprity.sprite import Sprite


class HernaSlucka:
    """
    Hlavná herná slučka, ktorá obsahuje a kontroluje všetky herné objekty.
    Používa sa staticky (nie je potrebné vytvárať viac ako jednu inštanciu).
    """

    OKNO = pygame.display.set_mode(n.VELKOST_OKNA)
    """Okno, v ktorom sa celá hra vykresľuje."""

    @staticmethod
    def spusti():
        """
        Spustí hlavnú hernú slučku.
        """

        HernaSlucka.initializuj()
        clock = pygame.time.Clock()

        while True:
            HernaSlucka.OKNO.fill((0, 0, 0))

            eventy = pygame.event.get()
            if not HernaSlucka.spracuj_eventy(eventy):
                break

            HernaSlucka.update()
            HernaSlucka.draw(HernaSlucka.OKNO)

            pygame.display.flip()
            clock.tick(60)

        pygame.quit()

    @staticmethod
    def initializuj():
        """
        Inicializuje pyGame a načíta všetky scény.
        """
        pygame.init()
        pygame.font.init()
        pygame.display.init()
        pygame.mixer.init()

        pygame.display.set_caption(n.NAZOV_HRY)
        Mixer.nacitat_zvuky()
        HernaSlucka.nacitat_sceny()

    @staticmethod
    def update():
        """
        Aktualizuje aktuálnu scénu.
        """
        ManazerScen.aktualna_scena().update()

    @staticmethod
    def draw(surface: pygame.Surface):
        """
        Vykresľuje aktuálnu scénu do daného okna.
        """

        ManazerScen.aktualna_scena().draw(surface)

    @staticmethod
    def nacitat_sceny():
        """
        Načíta všetky scény a nastaví prvú scénu ako aktuálnu.
        """
        ManazerScen.VSETKY_SCENY = [
            HlavneMenu(),
            Nastavenia(),
            Level("level_1"),
            KoniecHry(),
        ]
        ManazerScen.zmen_scenu(0)

    @staticmethod
    def spracuj_eventy(eventy: t.List[pygame.event.Event]) -> bool:
        """
        Pomocná funkcia pre spracovanie eventov.
        Ak vráti `False`, hlavná herná slučka sa zastaví (t. j. hru sme ukončili).
        """

        for event in eventy:
            if event.type == pygame.QUIT or (
                event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE
            ):
                return False  # ukončenie hry
            else:
                for sprite in ManazerScen.aktualna_scena().sprites():
                    if isinstance(sprite, Sprite):
                        sprite.spracuj_event(event, ManazerScen.aktualna_scena())

        return True
