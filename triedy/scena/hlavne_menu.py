from triedy.scena.scena import Scena
from triedy.ui import Tlacidlo


class HlavneMenu(Scena):
    def __init__(self):
        super().__init__(Tlacidlo((100, 100), "Hrať", lambda: self.zmen_scenu(1)))
