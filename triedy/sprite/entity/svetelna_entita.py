import typing as t

from triedy.sprite.entity.entita import Entita
from triedy.svetlo import Svetlo


class SvetelnaEntita(Entita):
    """
    Entita, ktorá emituje svetlo.
    """

    def __init__(
        self,
        pozicia: t.Tuple[int, int],
        velkost: t.Tuple[int, int],
        obrazok: str,
        rychlost=1.0,
        radius_svetla=80,
        intenzita_svetla=1.0,
        farba_svetla=(255, 255, 255),
    ):
        super().__init__(pozicia, velkost, obrazok, rychlost)
        self.svetlo = Svetlo(
            self.rect.center,
            radius_svetla,
            intenzita_svetla,
            farba_svetla,
        )

    def update(self):
        super().update()
        self.svetlo.pozicia = self.rect.center
