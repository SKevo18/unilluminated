import typing as t

import nastavenia as n
from triedy.mixer import Mixer
from triedy.sprity.entity.entita import Entita


class Truhla(Entita):
    """
    Ak sa hráč priblíži k truhle, otvorí sa a hráč zoberie kľúč od dverí.
    """

    def __init__(self, pozicia: t.Tuple[int, int]):
        super().__init__(
            pozicia,
            n.ASSETY_ROOT / "sprite" / "truhla",
            animacia_id="zatvorena",
        )

    def otvor(self) -> bool:
        """
        Pokúsi sa otvoriť truhlu.
        Vracia informáciu o tom, či bola truhla úspešne otvorená.
        """

        if not self.je_otvorena:
            self.id_aktualnej_animacie = "otvorena"
            Mixer.prehrat_zvuk("otvor")
            return True

        # nemôžme otvoriť už otvorenú truhlu
        return False

    @property
    def je_otvorena(self) -> bool:
        return self.id_aktualnej_animacie == "otvorena"
