import pygame

import nastavenia as n
from triedy.mixer import Mixer
from triedy.ui.text import Text
from triedy.sceny.scena import Scena
from triedy.ui.tlacidlo import Tlacidlo


class KoniecHry(Scena):
    """
    Scéna s koncom hry.
    """

    def __init__(self):
        stred = (n.VELKOST_OKNA[0] // 2, n.VELKOST_OKNA[1] // 2)
        koniec_hry = Text(stred, "Koniec hry!")
        koniec_hry.rect.center = (
            stred[0],
            stred[1] - koniec_hry.rect.height - 80,
        )

        hlavne_menu = Tlacidlo(stred, "Hlavné menu", lambda: self.zmen_scenu(0))
        hlavne_menu.rect.center = (stred[0] - hlavne_menu.rect.width / 2 - 20, stred[1])

        ukonci_tlacidlo = Tlacidlo(
            stred,
            "Ukončiť hru",
            lambda: pygame.event.post(pygame.event.Event(pygame.QUIT)),
        )
        ukonci_tlacidlo.rect.center = (
            stred[0] + ukonci_tlacidlo.rect.width / 2 + 20,
            stred[1],
        )

        super().__init__(koniec_hry, hlavne_menu, ukonci_tlacidlo)

    def pred_zmenou(self):
        Mixer.prehrat_pozadie()
