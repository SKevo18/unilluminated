import pygame

import nastavenia as n
from triedy.mixer import Mixer
from triedy.sceny.scena import Scena
from triedy.ui.tlacidlo import Tlacidlo


class HlavneMenu(Scena):
    """
    Hlavné menu hry a zároveň prvá scéna ktorá sa zobrazí.
    """

    def __init__(self):
        stred = (n.VELKOST_OKNA[0] // 2, n.VELKOST_OKNA[1] // 2)
        hrat_tlacidlo = Tlacidlo(stred, "Hrať", lambda: self.zmen_scenu(2))
        hrat_tlacidlo.rect.center = (
            stred[0],
            stred[1] - hrat_tlacidlo.rect.height - 20,
        )

        nastavenia_tlacidlo = Tlacidlo(stred, "Nastavenia", lambda: self.zmen_scenu(1))
        nastavenia_tlacidlo.rect.center = stred

        ukonci_tlacidlo = Tlacidlo(
            stred, "Ukončiť", lambda: pygame.event.post(pygame.event.Event(pygame.QUIT))
        )
        ukonci_tlacidlo.rect.center = (
            stred[0],
            stred[1] + nastavenia_tlacidlo.rect.height + 20,
        )

        super().__init__(hrat_tlacidlo, nastavenia_tlacidlo, ukonci_tlacidlo)

    def pred_zmenou(self):
        Mixer.prehrat_pozadie()
