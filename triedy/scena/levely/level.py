import pygame
import pytmx

from triedy.scena import Scena
from triedy.kamera import Kamera
from triedy.sprite import Sprite, Podlaha, Stena
from triedy.sprite.entity import Hrac


class Level(Scena):
    """
    Základná trieda pre všetky levely.
    """

    LEVELY_ROOT = Sprite.ASSETY_ROOT / "levely"

    def __init__(self, mapa_id: str):
        super().__init__()
        self.mapa_id = mapa_id
        self.hrac = None
        self.mapa = None

    def nacitat_level(self):
        self.mapa = pytmx.load_pygame(
            str(self.LEVELY_ROOT / f"{self.mapa_id}.tmx"), pixelalpha=True
        )

        podlaha: pytmx.TiledTileLayer = self.mapa.get_layer_by_name("podlaha")  # type: ignore
        steny: pytmx.TiledTileLayer = self.mapa.get_layer_by_name("steny")  # type: ignore
        entity: pytmx.TiledObjectGroup = self.mapa.get_layer_by_name("entity")  # type: ignore

        for x, y, image in podlaha.tiles():
            sprite = Podlaha((x * self.mapa.tilewidth, y * self.mapa.tileheight))
            sprite.image = image
            self.add(sprite)

        for x, y, image in steny.tiles():
            sprite = Stena((x * self.mapa.tilewidth, y * self.mapa.tileheight))
            sprite.image = image
            self.add(sprite)

        for obj in entity:
            self.hrac = Hrac((obj.x, obj.y))
            self.add(self.hrac)

    def skontroluj_kolizie(self):
        if not self.hrac:
            return

        kolizie_so_stenou = pygame.sprite.spritecollide(
            self.hrac,
            [s for s in self.sprites() if isinstance(s, Stena)], # type: ignore
            False,
        )

        if kolizie_so_stenou:
            self.hrac.rect.x = self.hrac.posledna_pozicia[0]
            self.hrac.rect.y = self.hrac.posledna_pozicia[1]

    def pred_zmenou(self):
        self.nacitat_level()

    def update(self):
        if not self.hrac:
            return

        super().update()
        Kamera.sleduj_entitu(self.hrac)
        self.skontroluj_kolizie()

    def draw(self, surface: pygame.Surface):
        for sprite in self.sprites():
            surface.blit(sprite.image, Kamera.aplikuj_na_sprite(sprite))
