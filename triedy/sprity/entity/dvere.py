import typing as t

import nastavenia as n
from triedy.mixer import Mixer
from triedy.sprity.entity.svetelna_entita import SvetelnaEntita


class Dvere(SvetelnaEntita):
    def __init__(self, pozicia: t.Tuple[int, int]):
        super().__init__(
            pozicia,
            n.ASSETY_ROOT / "sprite" / "dvere",
            animacia_id="zatvorene",
            radius_svetla=40,
            intenzita_svetla=1.0,
            farba_svetla=(0, 255, 255),
        )

    def otvor(self):
        self.id_aktualnej_animacie = "otvorene"
        Mixer.prehrat_zvuk("otvor")
