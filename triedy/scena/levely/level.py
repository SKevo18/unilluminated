import pygame
import pytmx

import nastavenia as n
from triedy.scena import Scena
from triedy.kamera import Kamera
from triedy.ui.text import Text
from triedy.sprite.sprite import Sprite
from triedy.sprite.podlaha import Podlaha
from triedy.sprite.stena import Stena
from triedy.sprite.entity.hrac import Hrac
from triedy.sprite.entity.entita import Entita
from triedy.sprite.entity.odrazajuca_prisera import OdrazajucaPrisera
from triedy.sprite.entity.svetelna_entita import SvetelnaEntita
from triedy.sprite.entity.priamociara_prisera import PriamociaraPrisera


class Level(Scena):
    """
    Základná trieda pre všetky levely.
    """

    LEVELY_ROOT = Sprite.ASSETY_ROOT / "levely"
    """Priečinok assetov s XML súbormi máp (pre pytmx)"""

    def __init__(self, mapa_id: str):
        super().__init__()
        self.mapa_id = mapa_id
        """ID mapy v assetoch."""

        self.hrac = None
        """Hráč."""
        self.mapa = None
        """Mapa levelu (Tiled)."""
        self.solidna_maska = None
        """Maska pre detekciu kolízií."""
        self.entity = pygame.sprite.Group()
        """Zoznam všetkých entít v leveli."""
        self.tmavy_povrch: pygame.Surface
        """Tmavý overlay pre celý level, na ktorý sa vykreslí svetlo."""

        self.text_hp = Text((100, 100), "HP: 100")
        """Textový objekt pre zobrazenie HP."""
        self.ui_elementy.add(self.text_hp)

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
        self.solidna_maska = pygame.mask.from_surface(maska_povrch)

        # spracovanie entít
        for obj in entity:
            if obj.name == "hrac":
                self.hrac = Hrac((obj.x, obj.y))
                self.entity.add(self.hrac)
            elif obj.name == "priamociara_prisera":
                self.entity.add(PriamociaraPrisera((obj.x, obj.y)))
            elif obj.name == "odrazajuca_prisera":
                self.entity.add(OdrazajucaPrisera((obj.x, obj.y)))
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

    def kontroluj_pohyb(self):
        """
        Kontroluje pohyb všetkých entít.
        """
        # level ešte nie je úplne načítaný
        if not self.hrac or not self.solidna_maska:
            return

        # nastavenie cielu pre všetky príšery
        # ktoré sa pohybujú priamo smerom k hráčovi
        PriamociaraPrisera.ciel = self.hrac.rect.center

        for entita in self.entity:
            if isinstance(entita, Entita):
                entita.pohyb(self.solidna_maska)

    def pred_zmenou(self):
        self.nacitat_level()

    def update(self):
        if not self.hrac:
            return

        super().update()
        Kamera.sleduj_entitu(self.hrac)
        self.kontroluj_pohyb()

    def draw(self, surface: pygame.Surface):
        # kópia z originálu, ktorú môžme upraviť
        # inak by tam bol after-image efekt
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
            # (pretože svetlo má menšiu transparentnosť ako tma, bude pri vykresľovan�� preferované)
            special_flags=pygame.BLEND_RGBA_MIN,
        )

        # vykreslenie UI elementov na konci (v screen-space)
        for ui_element in self.ui_elementy:
            surface.blit(ui_element.image, ui_element.rect)
