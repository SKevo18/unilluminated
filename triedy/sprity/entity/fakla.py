import typing as t

import nastavenia as n
from triedy.sprity.entity.svetelna_entita import SvetelnaEntita


class Fakla(SvetelnaEntita):
    """
    Pochodeň, ktorá vyžaruje (emituje) svetlo.
    Hráč ju môže položiť prostredníctvom "Space" (medzerníku).
    """

    def __init__(self, pozicia: t.Tuple[int, int]):
        super().__init__(
            pozicia,
            n.ASSETY_ROOT / "sprite" / "fakla",
            radius_svetla=60,
            intenzita_svetla=1.0,
            farba_svetla=(255, 255, 0),
        )
