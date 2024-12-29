import nastavenia as n
from triedy.mixer import Mixer
from triedy.sceny.scena import Scena
from triedy.ui.tlacidlo import Tlacidlo
from triedy.ui.zaskrtavacie_pole import ZaskrtavaciePole


class Nastavenia(Scena):
    """
    Nastavenia hry.
    """

    def __init__(self):
        stred = (n.VELKOST_OKNA[0] // 2, n.VELKOST_OKNA[1] // 2)
        radius_zp = 30
        poz_x = stred[0] - radius_zp * 3

        zvuky_zp = ZaskrtavaciePole(
            (poz_x, stred[1] - radius_zp * 5),
            radius_zp,
            "Zvuky",
            self.prepnut_zvuky,
            zaskrtnute=True,
        )

        hudba_zp = ZaskrtavaciePole(
            (poz_x, stred[1] - radius_zp * 2),
            radius_zp,
            "Hudba",
            self.prepnut_hudbu,
            zaskrtnute=True,
        )

        tlacidlo_spat = Tlacidlo(
            (poz_x, stred[1] + radius_zp),
            "Späť",
            lambda: Scena.zmen_scenu(0),
        )
        super().__init__(zvuky_zp, hudba_zp, tlacidlo_spat)

    @staticmethod
    def prepnut_zvuky(zapnute: bool):
        Mixer.zvuky_povolene = zapnute

    @staticmethod
    def prepnut_hudbu(zapnute: bool):
        Mixer.hudba_povolena = zapnute

        if zapnute:
            Mixer.prehrat_pozadie()
        else:
            Mixer.stop_pozadie()
