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
        pozicia: t.Tuple[int, int],
        velkost=(16, 16),
        cesta_k_obrazku: t.Optional[t.Union[Path, str]] = None,
    ):
        super().__init__()
        self.velkost = velkost
        self.image: pygame.Surface = pygame.Surface(velkost, pygame.SRCALPHA)
        if cesta_k_obrazku:
            self.image = self.nacitaj_obrazok(cesta_k_obrazku)

        self.rect: pygame.Rect = self.image.get_rect()
        self.rect.x = pozicia[0]
        self.rect.y = pozicia[1]

    def nacitaj_obrazok(self, cesta_k_obrazku: t.Union[Path, str]) -> pygame.Surface:
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
