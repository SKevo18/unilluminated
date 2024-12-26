"""
Modul pre hernú slučku.
"""

import typing as t

import asyncio
import pygame

import nastavenia as n
from triedy.scena import ManazerScen, HlavneMenu, Nastavenia
from triedy.scena.levely import Level1
from triedy.sprite.sprite import Sprite


class HernaSlucka:
    """
    Hlavná herná slučka, ktorá obsahuje a kontroluje všetky herné objekty.
    Používa sa staticky (nie je potrebné vytvárať viac ako jednu inštanciu).
    """

    OKNO = pygame.display.set_mode(n.VELKOST_OKNA)
    """Okno, v ktorom sa celá hra vykresľuje."""

    @staticmethod
    async def spusti():
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
            await asyncio.sleep(0)

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
        pygame.display.set_caption(n.NAZOV_HRY)
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
        ManazerScen.VSETKY_SCENY = [HlavneMenu(), Nastavenia(), Level1()]
        ManazerScen.zmen_scenu(0)

    @staticmethod
    def spracuj_eventy(eventy: t.List[pygame.event.Event]) -> bool:
        """
        Pomocná funkcia pre spracovanie eventov. Ak vráti `False`, hlavná herná slučka sa zastaví (t. j. hru sme ukončili).
        """

        for event in eventy:
            if event.type == pygame.QUIT or (
                event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE
            ):
                return False  # ukončenie hry
            else:
                for sprite in ManazerScen.aktualna_scena().sprites():
                    if isinstance(sprite, Sprite):
                        sprite.spracuj_event(event)

        return True
