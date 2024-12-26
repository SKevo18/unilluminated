"""
Modul pre hernú slučku.
"""

import pygame
import pygame_widgets

import nastavenia as n
from triedy.scena import ManazerScen, HlavneMenu, Level1
from triedy.ui.tlacidlo import Tlacidlo


class HernaSlucka:
    """
    Hlavná herná slučka, ktorá obsahuje a kontroluje všetky herné objekty.
    Používa sa staticky (nie je potrebné vytvárať viac ako jednu inštanciu).
    """

    OKNO = pygame.display.set_mode(n.VELKOST_OKNA)
    """Okno, v ktorom sa celá hra vykresľuje."""
    CLOCK = pygame.time.Clock()

    @staticmethod
    def spusti():
        """
        Spustí hlavnú hernú slučku.
        """
        HernaSlucka.initializuj()

        bezi = True
        while bezi:
            HernaSlucka.OKNO.fill((0, 0, 0))

            eventy = pygame.event.get()
            if not HernaSlucka._spracuj_eventy(eventy):
                bezi = False
                break
            HernaSlucka.update()
            HernaSlucka.draw(HernaSlucka.OKNO)

            pygame_widgets.update(eventy)
            pygame.display.flip()
            HernaSlucka.CLOCK.tick(60)

        pygame.quit()
        exit()

    @staticmethod
    def initializuj():
        """
        Inicializuje pyGame a načíta všetky scény.
        """
        pygame.init()
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
        ManazerScen.VSETKY_SCENY = [HlavneMenu(), Level1()]
        ManazerScen.zmen_scenu(0)

    @staticmethod
    def _spracuj_eventy(eventy: list[pygame.event.Event]) -> bool:
        """
        Pomocná funkcia pre spracovanie eventov. Ak vráti `False`, hlavná herná slučka sa zastaví (t. j. hru sme ukončili).
        """

        for event in eventy:
            if event.type == pygame.QUIT or (
                event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE
            ):
                return False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                for tlacidlo in ManazerScen.aktualna_scena().sprites():
                    if isinstance(tlacidlo, Tlacidlo):
                        if tlacidlo.rect.collidepoint(event.pos):
                            tlacidlo.po_kliknuti()
                            return True
        return True
