import typing as t

import nastavenia as n
from triedy.sprity.entity.svetelna_entita import SvetelnaEntita


class Truhla(SvetelnaEntita):
    def __init__(self, pozicia: t.Tuple[int, int]):
        super().__init__(
            pozicia,
            n.ASSETY_ROOT / "sprite" / "truhla",
            animacia_id="zatvorena",
            radius_svetla=40,
            intenzita_svetla=0.5,
            farba_svetla=(0, 255, 255),
        )

    def otvor(self):
        self.animacia_id = "otvorena"
