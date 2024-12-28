import typing as t
from pathlib import Path

import pygame

from triedy.sprite.sprite import Sprite


class AnimovanySprite(Sprite):
    """
    Predstavuje animovaný sprite.
    """

    CACHE_ANIMACII: t.Dict[str, t.List[pygame.Surface]] = {}

    def __init__(
        self,
        pozicia: t.Tuple[int, int],
        root_priecinok_animacii: t.Union[Path, str],
        velkost=(16, 16),
        animacia_id="chill",
    ):
        super().__init__(pozicia, velkost, None)
        self.id_aktualnej_animacie = animacia_id
        """ID aktuálnej animácie ktorá sa prehráva."""
        self.animuj = True
        """Ak je `True`, obrázky sa menia v metóde `update()`."""

        self._aktualna_je_jednorazova = False
        """Ak je `True`, aktuálna animácia sa prehrá len jedenkrát."""
        self._predchadzajuca_animacia = animacia_id
        """Pomocná premenná na ukladanie predchádzajúcej animácie."""
        self._cas_animacie = 0
        """Čas animácie v milisekundách (pre výpočet indexu)."""

        self.nacitaj_animacie(root_priecinok_animacii)

    def zmen_animaciu(self, nova_animacia_id: str):
        if nova_animacia_id in self.CACHE_ANIMACII:
            self.id_aktualnej_animacie = nova_animacia_id
            self._cas_animacie = 0
        else:
            raise ValueError(f"Animácia '{nova_animacia_id}' neexistuje!")

    def nacitaj_animacie(
        self,
        root_priecinok_animacii: t.Union[Path, str],
    ):
        """
        Načíta všetky animácie z daného adresára.
        Ak už existujú animácie v cache, vráti ich.

        `@classmethod` preto, aby každý potomok mal svoj vlastný cache.
        """

        # konverzia na `Path` objekt
        if isinstance(root_priecinok_animacii, str):
            root_priecinok_animacii = Path(root_priecinok_animacii)

        for animacia_priecinok in root_priecinok_animacii.iterdir():
            # /<root_priecinok_animacii>/<id_animacie>/0..n.png
            id_animacie = animacia_priecinok.name

            self.CACHE_ANIMACII[id_animacie] = []
            if not animacia_priecinok.exists():
                raise ValueError(f"Adresár animácií `{animacia_priecinok}` neexistuje!")

            # načítame všetky animácie a uložíme do cache
            for subor_frame in animacia_priecinok.iterdir():
                obrazok = pygame.image.load(subor_frame).convert_alpha()
                self.CACHE_ANIMACII[id_animacie].append(obrazok)

    @property
    def animacie(self):
        """
        Vráti sekvenciu (zoznam) obrázkov aktuálnej animácie.
        """

        try:
            return self.CACHE_ANIMACII[self.id_aktualnej_animacie]
        except KeyError:
            raise ValueError(f"Animácia '{self.id_aktualnej_animacie}' neexistuje!")

    def prehrat_animaciu(self, animacia_id: str):
        """
        Prehrá animáciu jedenkrát a potom sa vráti k predchádzajúcej animácii.
        """

        self._predchadzajuca_animacia = self.id_aktualnej_animacie
        self.zmen_animaciu(animacia_id)
        self._aktualna_je_jednorazova = True

    def update(self):
        if self.id_aktualnej_animacie is None:
            return super().update()
        if self.animuj:
            self._cas_animacie += 1

        pocet_framov = len(self.animacie)
        index = self._cas_animacie // 10 % pocet_framov

        # kontrola ukončenia jednorazovej animácie - čakáme na koniec celej animácie
        if self._aktualna_je_jednorazova and self._cas_animacie >= pocet_framov * 10:
            self._aktualna_je_jednorazova = False
            self.zmen_animaciu(self._predchadzajuca_animacia)  # vrátime sa na pôvodnú

        # načítanie aktuálneho obrázku animácie (ak index existuje)
        try:
            self.originalny_obrazok = self.animacie[index].copy()
        except IndexError:
            print(
                f"Animácia '{self.id_aktualnej_animacie}' s indexom `{index}` nemá dostatočný počet obrázkov (alebo je neplatný index)."
            )

            # fallback na prvý obrázok, aby nespadla celá hra:
            self.originalny_obrazok = self.animacie[0].copy()

        # otočenie
        if self.je_otoceny:
            self.originalny_obrazok = pygame.transform.flip(
                self.originalny_obrazok, True, False
            )

        # kamera nastaví self.image z self.originalny_obrazok
        return super().update()
