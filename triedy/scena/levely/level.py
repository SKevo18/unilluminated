import pygame
import pytmx

from triedy.scena import Scena
from triedy.kamera import Kamera
from triedy.sprite import Sprite
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

        for layer in self.mapa.visible_layers:
            if isinstance(layer, pytmx.TiledTileLayer):
                for x, y, gid, *_ in layer.iter_data():
                    tile = self.mapa.get_tile_image_by_gid(gid)
                    if tile:
                        sprite = Sprite(
                            (x * self.mapa.tilewidth, y * self.mapa.tileheight)
                        )
                        sprite.image = tile
                        self.add(sprite)
            elif isinstance(layer, pytmx.TiledObjectGroup):
                for obj in layer:
                    if obj.name == "hrac":
                        self.hrac = Hrac((obj.x, obj.y))
                        print(self.hrac)
                        self.add(self.hrac)

    def pred_zmenou(self):
        self.nacitat_level()

    def update(self):
        super().update()
        if self.hrac:
            Kamera.sleduj_entitu(self.hrac)

    def draw(self, surface: pygame.Surface):
        for sprite in self.sprites():
            surface.blit(sprite.image, Kamera.aplikuj_na_sprite(sprite))
