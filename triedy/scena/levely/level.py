import pygame
import pytmx

import nastavenia as n
from triedy.scena import Scena
from triedy.kamera import Kamera
from triedy.sprite import Sprite, Podlaha, Stena
from triedy.sprite.entity import Hrac
from triedy.sprite.entity.entita import Entita
from triedy.sprite.entity.svetelna_entita import SvetelnaEntita


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

        self.tmavy_povrch: pygame.Surface
        """Tmavý overlay pre celý level."""

    def nacitat_level(self):
        self.mapa = pytmx.load_pygame(
            str(self.LEVELY_ROOT / f"{self.mapa_id}.tmx"), pixelalpha=True
        )
        self.velkost_spritu = self.mapa.tilewidth

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
        self.add(self.entity)

        # celý level je zakrytý tmavým povrchom
        # na ktorý sa vykreslí svetlo
        self.tmavy_povrch = pygame.Surface(
            (
                n.VELKOST_OKNA[0],
                n.VELKOST_OKNA[1],
            ),
            pygame.SRCALPHA,
        )
        self.tmavy_povrch.fill((0, 0, 0))

    def skontroluj_kolizie(self):
        if not self.steny_maska:
            return

        for entita in self.entity:
            if not isinstance(entita, Entita) or not entita.velocita.length():
                continue

            # pohyb po X osi
            nove_x = entita.rect.x + entita.velocita.x
            maska_pozicia = (nove_x, entita.rect.y + entita.maska_offset[1])
            if not self.steny_maska.overlap(entita.maska, maska_pozicia):
                entita.rect.x = nove_x

            # pohyb po Y osi
            nove_y = entita.rect.y + entita.velocita.y
            maska_pozicia = (entita.rect.x, nove_y + entita.maska_offset[1])
            if not self.steny_maska.overlap(entita.maska, maska_pozicia):
                entita.rect.y = nove_y

    def pred_zmenou(self):
        self.nacitat_level()

    def update(self):
        if not self.hrac:
            return

        super().update()
        Kamera.sleduj_entitu(self.hrac)
        self.skontroluj_kolizie()

    def draw(self, surface: pygame.Surface):
        tmavy_povrch = self.tmavy_povrch.copy()

        # zoradenie spritov podľa Y pozície (hĺbky)
        for sprite in sorted(
            self.sprites(),
            key=lambda sprite: [
                not isinstance(
                    sprite,
                    Podlaha,  # podlaha sa vykresľuje prvá
                ),
                sprite.rect.y,  # ...inak sa kreslí podľa Y
            ],
        ):
            # vykreslenie svetla
            if isinstance(sprite, SvetelnaEntita):
                sprite.svetlo.aplikuj_na_tmu(tmavy_povrch)

            # vykreslenie sprite, s ohľadom na zoom a pozíciu kamery
            surface.blit(sprite.image, Kamera.aplikuj_na_sprite(sprite))

        surface.blit(
            tmavy_povrch,
            (0, 0),
            # ak miešame pixel, preferujeme ten s menšou transparentnosťou
            # vďaka tomu sa "vyreže" svetlo do tmy
            # (pretože svetlo má menšiu transparentnosť ako tma, bude pri vykresľovaní preferované)
            special_flags=pygame.BLEND_RGBA_MIN,
        )
