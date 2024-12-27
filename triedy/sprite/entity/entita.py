import typing as t

import pygame

from triedy.sprite.sprite import Sprite


class Entita(Sprite):
    """
    Základná trieda pre všetky entity.
    """

    def __init__(
        self,
        pozicia: t.Tuple[int, int],
        velkost: t.Tuple[int, int],
        obrazok: str,
        rychlost=1,
    ):
        super().__init__(pozicia, velkost, obrazok)
        maska_vyska = self.rect.height // 5
        self.velocita = pygame.Vector2(0, 0)
        """Aktuálny smer pohybu."""
        self.rychlost = rychlost
        """Rýchlosť pohybu."""

        self.maska = pygame.Mask((self.rect.width, maska_vyska), True)
        """Maska pre detekciu kolízií. Neprekrýva celé telo, aby bola zachovaná ilúzia priestoru (torso bude hore trčať)."""
        self.maska_offset = (0, self.rect.height - maska_vyska)
        """Offset pre detekciu kolízií."""
        self.posledna_pozicia: t.Optional[t.Tuple[int, int]] = None
        """Pre detekciu kolízií."""
