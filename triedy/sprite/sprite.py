import typing as t

from pathlib import Path
import pygame


class Sprite(pygame.sprite.Sprite):
    """
    Predstavuje všetky interaktívne objekty v hre.
    """

    ASSETY_ROOT = Path(__file__).parent.parent.parent / "assety"

    def __init__(
        self,
        pozicia: tuple[int, int],
        velkost: tuple[int, int],
        cesta_k_obrazku: t.Optional[Path | str] = None,
    ):
        super().__init__()
        self.velkost = velkost
        if cesta_k_obrazku:
            self.image = self.nacitaj_obrazok(cesta_k_obrazku)
        else:
            self.image = pygame.Surface(velkost, pygame.SRCALPHA)

        self.rect = self.image.get_rect()
        self.rect.x = pozicia[0]
        self.rect.y = pozicia[1]

    def nacitaj_obrazok(self, cesta_k_obrazku: Path | str) -> pygame.Surface:
        """
        Nacitá obrazok z daného adresára (relatívneho ku `ASSETY_ROOT`) a nastaví ho na správnu velkosť.
        Vráti načítaný obrázok.
        """

        obrazok = pygame.image.load(self.ASSETY_ROOT / cesta_k_obrazku).convert_alpha()
        obrazok = pygame.transform.scale(obrazok, self.velkost)

        return obrazok

    def spracuj_event(self, _: pygame.event.Event):
        """
        Spracuje event z hlavnej hernej slučky.
        """
        pass
