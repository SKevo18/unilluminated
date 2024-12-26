import typing as t

# aby nebol circular import - scena importuje manazera aby zmenila scenu
if t.TYPE_CHECKING:
    from triedy.scena.scena import Scena

import pygame


class ManazerScen:
    """
    Manažér scén. Používa sa staticky (nie je potrebné vytvárať viac ako jednu inštanciu).
    """

    VSETKY_SCENY: t.List["Scena"] = []
    """Všetky scény v hre."""
    index_aktualnej_sceny = 0
    """Index aktuálnej scény, ktorá sa vykresľuje v hernej slučke."""

    @staticmethod
    def zmen_scenu(index: int):
        ManazerScen.index_aktualnej_sceny = index

    @staticmethod
    def aktualna_scena() -> "Scena":
        try:
            return ManazerScen.VSETKY_SCENY[ManazerScen.index_aktualnej_sceny]
        except IndexError:
            raise ValueError(f"Index aktuálnej scény ({ManazerScen.index_aktualnej_sceny}) neexistuje!")

    @staticmethod
    def update():
        """
        Aktualizuje aktuálnu scénu.
        """
        ManazerScen.aktualna_scena().update()

    @staticmethod
    def draw(surface: pygame.Surface):
        """
        Vykresľuje aktuálnu scénu do daného okna.
        """
        ManazerScen.aktualna_scena().draw(surface)
