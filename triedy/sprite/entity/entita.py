import typing as t

from pathlib import Path
import pygame

from triedy.sprite.animovany_sprite import AnimovanySprite


class Entita(AnimovanySprite):
    """
    Základná trieda pre všetky entity.
    """

    def __init__(
        self,
        pozicia: t.Tuple[int, int],
        velkost: t.Tuple[int, int],
        animacia_id: t.Optional[str] = None,
        cesta_k_obrazkom: t.Optional[t.Union[Path, str]] = None,
        # rýchlosť vyššia ako 1 spôsobí, že detekcia kolízií nebude fungovať
        # (preskočia sa framy)
        rychlost=0.2,
    ):
        super().__init__(pozicia, velkost, animacia_id, cesta_k_obrazkom)
        maska_vyska = self.rect.height // 5
        self.velocita = pygame.Vector2(0, 0)
        """Aktuálny smer pohybu."""
        self.rychlost = rychlost
        """Rýchlosť pohybu."""

        self.maska = pygame.Mask((self.rect.width, maska_vyska), True)
        """Maska pre detekciu kolízií. Neprekrýva celé telo, aby bola zachovaná ilúzia priestoru (torso bude hore trčať)."""
        self.maska_offset = (0, self.rect.height - maska_vyska)
        """Offset pre detekciu kolízií, relatívne od ľavého horného rohu postavy (maska sa nachádza dole pri nohách)."""
        self.posledna_pozicia: t.Optional[t.Tuple[int, int]] = None
        """Pre detekciu kolízií."""
