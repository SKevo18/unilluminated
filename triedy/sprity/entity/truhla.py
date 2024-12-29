import typing as t

import nastavenia as n
from triedy.mixer import Mixer
from triedy.sprity.entity.entita import Entita


class Truhla(Entita):
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

        return False

    @property
    def je_otvorena(self) -> bool:
        return self.id_aktualnej_animacie == "otvorena"
