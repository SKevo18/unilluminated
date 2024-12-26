import nastavenia as n
from triedy.scena import Scena
from triedy.ui import ZaskrtavaciePole, Tlacidlo


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
            lambda zaskrtnute: print("test zvuky:", zaskrtnute),
            zaskrtnute=True,
        )

        hudba_zp = ZaskrtavaciePole(
            (poz_x, stred[1] - radius_zp * 2),
            radius_zp,
            "Hudba",
            lambda zaskrtnute: print("test hudba:", zaskrtnute),
            zaskrtnute=True,
        )

        tlacidlo_spat = Tlacidlo(
            (poz_x, stred[1] + radius_zp),
            "Späť",
            lambda: Scena.zmen_scenu(0),
        )
        super().__init__(zvuky_zp, hudba_zp, tlacidlo_spat)
