import pygame
import pytmx

from triedy.scena import Scena
from triedy.kamera import Kamera
from triedy.sprite import Sprite, Podlaha, Stena
from triedy.sprite.entity import Hrac
from triedy.sprite.entity.entita import Entita


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
        self.steny_maska = None
        self.entity = pygame.sprite.Group()

    def nacitat_level(self):
        self.mapa = pytmx.load_pygame(
            str(self.LEVELY_ROOT / f"{self.mapa_id}.tmx"), pixelalpha=True
        )

        podlaha: pytmx.TiledTileLayer = self.mapa.get_layer_by_name("podlaha")  # type: ignore
        steny: pytmx.TiledTileLayer = self.mapa.get_layer_by_name("steny")  # type: ignore
        entity: pytmx.TiledObjectGroup = self.mapa.get_layer_by_name("entity")  # type: ignore

        # vytvorenie kociek podlahy:
        for x, y, image in podlaha.tiles():
            sprite = Podlaha((x * self.mapa.tilewidth, y * self.mapa.tileheight))
            sprite.image = image
            self.add(sprite)

        # vytvorenie dočasného povrchu pre steny
        # (z tohto sa neskôr vytvorí maska pre detekciu kolízií)
        maska_povrch = pygame.Surface(
            (
                self.mapa.width * self.mapa.tilewidth,
                self.mapa.height * self.mapa.tileheight,
            ),
            pygame.SRCALPHA,
        )

        for x, y, image in steny.tiles():
            pozicia = (x * self.mapa.tilewidth, y * self.mapa.tileheight)
            sprite = Stena(pozicia)
            sprite.image = image
            self.add(sprite)
            maska_povrch.blit(image, pozicia)

        # konverzia dočasného povrchu stien na masku
        # (detekcia kolízií cez masky je oveľakrát rýchlejšia a nespôsobuje problémy s výkonom)
        self.steny_maska = pygame.mask.from_surface(maska_povrch)

        # spracovanie entít
        for obj in entity:
            self.hrac = Hrac((obj.x, obj.y))
            self.entity.add(self.hrac)
            self.add(self.hrac)

    def skontroluj_kolizie(self):
        if not self.steny_maska:
            return

        # FIXME: mieša sa Hrac.update a skontroluj_kolizie
        for entita in self.entity:
            if not isinstance(entita, Entita) or not entita.velocita.length():
                continue

            entita.posledna_pozicia = entita.rect.x, entita.rect.y
            povodna_rychlost = entita.rychlost

            # pohyb po X osi
            entita.rect.x = entita.posledna_pozicia[0] + entita.velocita.x
            maska_pozicia = (entita.rect.x, entita.rect.y + entita.maska_offset[1])
            if self.steny_maska.overlap(entita.maska, maska_pozicia):
                entita.rect.x = entita.posledna_pozicia[0]
                entita.rychlost = 0

            # pohyb po Y osi
            entita.rect.y = entita.posledna_pozicia[1] + entita.velocita.y
            maska_pozicia = (entita.rect.x, entita.rect.y + entita.maska_offset[1])
            if self.steny_maska.overlap(entita.maska, maska_pozicia):
                entita.rect.y = entita.posledna_pozicia[1]
                entita.rychlost = 0

            # ak sme narazili do steny, obnovíme velocitu pre ďalší frame
            if entita.rychlost <= 0:
                entita.rychlost = povodna_rychlost

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
