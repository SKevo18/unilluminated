from pathlib import Path
import typing as t

from triedy.sprity.entity.svetelna_entita import SvetelnaEntita


class Prisera(SvetelnaEntita):
    """
    Všeobecná príšera ktorá ubližuje hráčovi.
    """

    def __init__(
        self,
        pozicia: t.Tuple[int, int],
        root_priecinok_animacii: t.Union[Path, str],
        velkost=(11, 16),
        animacia_id="zakladna",
        rychlost=0.3,
        # predvolene neemituje svetlo
        radius_svetla=0,
        rozsah_pulzovania=0,
        intenzita_svetla=0.0,
        farba_svetla=(0, 0, 0),
    ):
        super().__init__(
            pozicia,
            root_priecinok_animacii,
            velkost,
            animacia_id,
            rychlost,
            radius_svetla,
            rozsah_pulzovania,
            intenzita_svetla,
            farba_svetla,
        )
