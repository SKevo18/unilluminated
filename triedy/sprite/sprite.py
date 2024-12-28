import typing as t

if t.TYPE_CHECKING:
    from triedy.scena import Scena

from pathlib import Path
import pygame


class Sprite(pygame.sprite.Sprite):
    """
    Predstavuje všetky interaktívne objekty v hre.
    """

    ASSETY_ROOT = Path(__file__).parent.parent.parent / "assets"

    def __init__(
        self,
        pozicia: t.Tuple[int, int],
        velkost=(16, 16),
        cesta_k_obrazku: t.Optional[t.Union[Path, str]] = None,
        je_otoceny=False,
    ):
        super().__init__()
        self.velkost = velkost
        self.je_otoceny = je_otoceny

        # self.image je v mojom prípade vždy pygame.Surface,
        # nikdy nie `None` ako to hovoria typy v pygame-ce
        # inak by mi editor hlásil chybu všade kde používam niečo nad `image`
        self.image: pygame.Surface
        if cesta_k_obrazku:
            self.image = self.nacitaj_obrazok(cesta_k_obrazku)
        else:
            self.image = pygame.Surface(velkost, pygame.SRCALPHA)

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

        if self.je_otoceny:
            obrazok = pygame.transform.flip(obrazok, True, False)

        return obrazok

    def spracuj_event(self, event: pygame.event.Event, aktualna_scena: "Scena"):
        """
        Spracuje event z hlavnej hernej slučky.
        """
        pass
