from pathlib import Path

import nastavenia as n
from triedy.sprity.sprite import Sprite


class ZobratyKluc(Sprite):
    def __init__(self):
        pozicia = (10, n.VELKOST_OKNA[1] - 35)
        super().__init__(pozicia, (32, 32))
        self.kluc = self.nacitaj_obrazok(Path("ui") / "kluc.png")

    def zobraz(self):
        self.image.blit(self.kluc, (0, 0))
