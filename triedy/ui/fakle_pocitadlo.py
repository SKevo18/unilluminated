import typing as t

from triedy.ui.text import Text


class FaklePocitadlo(Text):
    """
    Počítadlo pochodní, ktoré má hráč k dispozícií.
    """

    def __init__(self, pozicia: t.Tuple[int, int], pocet_fakli=3):
        self._pocet_fakli = pocet_fakli
        super().__init__(
            pozicia, f"Fakle: {self._pocet_fakli}", 20, (255, 255, 0), (0, 0, 0)
        )

    @property
    def pocet_fakli(self) -> int:
        """
        Počet pochodní (faklí).
        """

        return self._pocet_fakli

    @pocet_fakli.setter
    def pocet_fakli(self, novy_pocet: int):
        """
        Setter pre počet sŕdc, ktorý znovu vykreslí srdcia po zmene.
        """

        self._pocet_fakli = novy_pocet
        self.text = f"Fakle: {self._pocet_fakli}"
