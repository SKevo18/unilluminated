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
        root_priecinok_animacii: t.Union[Path, str],
        velkost=(16, 16),
        animacia_id: str = "chill",
        # rýchlosť vyššia ako 1 spôsobí, že detekcia kolízií nebude fungovať
        # (preskočia sa framy):
        rychlost=0.2,
    ):
        super().__init__(pozicia, root_priecinok_animacii, velkost, animacia_id)
        maska_vyska = self.rect.height // 5

        self.pozicia = pygame.Vector2(pozicia)
        """
        Pozícia entity vo vektorovej forme, na desatinnú presnosť.
        Je to z toho dôvodu, že `pygame.Rect` je zaokrúhlené na celé čísla,
        no moja rýchlosť entít je v malých desatinných číslach.

        Zaokrúhlenie priamo cez `pygame.Rect` by spôsobilo, že entita sa
        napr. nebude môcť pohybovať v pozitívnom smere osi X alebo Y.
        """

        self.velocita = pygame.Vector2(0, 0)
        """Aktuálny smer pohybu."""
        self.rychlost = rychlost
        """Rýchlosť pohybu."""
        self.moze_ist = True
        """Ak je `True`, entita má povolené sa hýbať (pohyb je kontrolovaný v `Level.hyb_entitami()`)."""

        self.maska = pygame.Mask((self.rect.width, maska_vyska), True)
        """Maska pre detekciu kolízií. Neprekrýva celé telo, aby bola zachovaná ilúzia priestoru (torso bude hore trčať)."""
        self.maska_offset = (0, self.rect.height - maska_vyska)
        """Offset pre detekciu kolízií, relatívne od ľavého horného rohu postavy (maska sa nachádza dole pri nohách)."""

    def pohyb(self, solidna_maska: pygame.mask.Mask):
        """
        Kontroluje pohyb entity, ak je to možné.
        """

        if not self.moze_ist:
            return

        # pohyb po X osi
        nove_x = self.pozicia.x + self.velocita.x
        maska_pozicia = (nove_x, self.rect.y + self.maska_offset[1])
        if not solidna_maska.overlap(self.maska, maska_pozicia):
            self.pozicia.x = nove_x

        # pohyb po Y osi
        nove_y = self.pozicia.y + self.velocita.y
        maska_pozicia = (self.pozicia.x, nove_y + self.maska_offset[1])
        if not solidna_maska.overlap(self.maska, maska_pozicia):
            self.pozicia.y = nove_y

        self.rect.topleft = self.pozicia
