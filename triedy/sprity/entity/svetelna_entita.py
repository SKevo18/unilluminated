import typing as t
from pathlib import Path

from triedy.sprity.entity.entita import Entita
from triedy.svetlo import Svetlo


class SvetelnaEntita(Entita):
    """
    Entita, ktorá emituje svetlo.
    """

    def __init__(
        self,
        pozicia: t.Tuple[int, int],
        root_priecinok_animacii: t.Union[Path, str],
        velkost=(16, 16),
        animacia_id="zakladna",
        rychlost=1.0,
        radius_svetla=80,
        rozsah_pulzovania=3,
        intenzita_svetla=1.0,
        farba_svetla=(255, 255, 255),
    ):
        super().__init__(
            pozicia, root_priecinok_animacii, velkost, animacia_id, rychlost
        )
        self.svetlo = Svetlo(
            self.rect.center,
            radius_svetla,
            rozsah_pulzovania,
            intenzita_svetla,
            farba_svetla,
        )

    def update(self):
        self.svetlo.pozicia = self.rect.center
        return super().update()
