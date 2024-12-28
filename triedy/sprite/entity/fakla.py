import typing as t

from triedy.sprite.entity.svetelna_entita import SvetelnaEntita


class Fakla(SvetelnaEntita):
    def __init__(self, pozicia: t.Tuple[int, int]):
        super().__init__(
            pozicia,
            self.ASSETY_ROOT / "sprite" / "fakla",
            radius_svetla=80,
            intenzita_svetla=0.75,
            farba_svetla=(255, 100, 0),
        )

    
