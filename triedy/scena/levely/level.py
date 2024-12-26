from pathlib import Path
import pytmx

from triedy.scena import Scena
from triedy.sprite import Sprite
from triedy.sprite.entity import Hrac


class Level(Scena):
    """
    Základná trieda pre všetky levely.
    """

    LEVELY_ROOT = Path(__file__).parent.parent.parent.parent / "assety" / "levely"

    def __init__(self, mapa_id: str):
        super().__init__()
        self.nacitat_level(mapa_id)

    def nacitat_level(self, mapa_id: str):
        self.mapa = pytmx.load_pygame(
            str(self.LEVELY_ROOT / f"{mapa_id}.tmx"), pixelalpha=True
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
                        hrac = Hrac((obj.x, obj.y))
                        self.add(hrac)
