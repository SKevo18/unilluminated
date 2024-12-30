import pygame
import pytmx

import nastavenia as n
from triedy.kamera import Kamera
from triedy.mixer import Mixer
from triedy.sceny.scena import Scena
from triedy.sprity.entity.dvere import Dvere
from triedy.sprity.entity.entita import Entita
from triedy.sprity.entity.hrac import Hrac
from triedy.sprity.entity.odrazajuca_prisera import OdrazajucaPrisera
from triedy.sprity.entity.priamociara_prisera import PriamociaraPrisera
from triedy.sprity.entity.prisera import Prisera
from triedy.sprity.entity.svetelna_entita import SvetelnaEntita
from triedy.sprity.entity.truhla import Truhla
from triedy.sprity.podlaha import Podlaha
from triedy.sprity.stena import Stena
from triedy.sprity.dekoracia import Dekoracia, DekoraciaZem


class Level(Scena):
    """
    Základná trieda pre všetky levely.
    """

    LEVELY_ROOT = n.ASSETY_ROOT / "levely"
    """Priečinok assetov s XML súbormi máp (pre pytmx)"""

    def __init__(self, mapa_id: str):
        super().__init__()
        self.mapa_id = mapa_id
        """ID mapy v assetoch."""

        self.hrac: Hrac
        """Hráč."""
        self.mapa = None
        """Mapa levelu (Tiled)."""
        self.solidna_maska = None
        """Maska pre detekciu kolízií."""
        self.entity = pygame.sprite.Group()
        """Zoznam všetkých entít v leveli."""
        self.tmavy_povrch: pygame.Surface
        """Tmavý overlay pre celý level, na ktorý sa vykreslí svetlo."""

    def nacitat_level(self):
        self.mapa = pytmx.load_pygame(str(self.LEVELY_ROOT / f"{self.mapa_id}.tmx"))
        self.velkost_spritu = self.mapa.tilewidth

        podlahy: pytmx.TiledTileLayer = self.mapa.get_layer_by_name("podlaha")  # type: ignore
        dekoracie: pytmx.TiledTileLayer = self.mapa.get_layer_by_name("dekoracie")  # type: ignore
        dekoracie_zem: pytmx.TiledTileLayer = self.mapa.get_layer_by_name("dekoracie_zem")  # type: ignore
        steny: pytmx.TiledTileLayer = self.mapa.get_layer_by_name("steny")  # type: ignore
        entity: pytmx.TiledObjectGroup = self.mapa.get_layer_by_name("entity")  # type: ignore

        # vytvorenie kociek podlahy:
        for x, y, image in podlahy.tiles():
            podlaha = Podlaha((x * self.mapa.tilewidth, y * self.mapa.tileheight))
            podlaha.image = image
            self.add(podlaha)
    
        # dekorácie nemajú kolíziu
        for x, y, image in dekoracie.tiles():
            dekoracia = Dekoracia((x * self.mapa.tilewidth, y * self.mapa.tileheight))
            dekoracia.image = image
            self.add(dekoracia)
    
        # dekorácie na zemi nemajú "hĺbku"
        for x, y, image in dekoracie_zem.tiles():
            dekoracia_zem = DekoraciaZem((x * self.mapa.tilewidth, y * self.mapa.tileheight))
            dekoracia_zem.image = image
            self.add(dekoracia_zem)

        # vytvorenie dočasného povrchu pre steny
        # (z tohto sa neskôr vytvorí maska pre detekciu kolízií)
        maska_povrch = pygame.Surface(
            (
                self.mapa.width * self.mapa.tilewidth,
                self.mapa.height * self.mapa.tileheight,
            ),
            pygame.SRCALPHA,
        )

        maska_surface = pygame.Surface(
            (16, 16),
            masks=(0, 0, 0),  # dočasná maska pre solidné objekty
        )
        for x, y, image in steny.tiles():
            pozicia = (x * self.mapa.tilewidth, y * self.mapa.tileheight)
            stena = Stena(pozicia)
            stena.image = image
            self.add(stena)
            maska_povrch.blit(maska_surface, pozicia)

        # spracovanie entít
        for obj in entity:
            if obj.name == "hrac":
                self.hrac = Hrac((obj.x, obj.y))
                self.entity.add(self.hrac)
            elif obj.name == "priamociara_prisera":
                self.entity.add(PriamociaraPrisera((obj.x, obj.y)))
            elif obj.name == "odrazajuca_prisera":
                self.entity.add(OdrazajucaPrisera((obj.x, obj.y)))

            # solidné (majú masku):
            elif obj.name == "truhla":
                self.entity.add(Truhla((obj.x, obj.y)))
                maska_povrch.blit(maska_surface, (obj.x, obj.y))
            elif obj.name == "dvere":
                self.entity.add(Dvere((obj.x, obj.y)))
                maska_povrch.blit(maska_surface, (obj.x, obj.y))
        self.add(self.entity)

        # konverzia dočasného povrchu stien na masku
        # (detekcia kolízií cez masky je oveľakrát rýchlejšia a nespôsobuje problémy s výkonom)
        self.solidna_maska = pygame.mask.from_surface(maska_povrch)

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

        # pridať UI elementy pre hráča
        self.ui_elementy.append(self.hrac.pocitadlo_fakli)
        self.ui_elementy.append(self.hrac.pocitadlo_zivotov)
        self.ui_elementy.append(self.hrac.zobraty_kluc)

    def pred_zmenou(self):
        self.nacitat_level()

    def pred_zmenou_na_dalsiu(self):
        # upraceme po sebe, aby tam nič nebolo
        # ak sa vrátime na ten istý level:
        self.empty()
        self.entity.empty()
        self.hrac.zivoty = 3
        self.ui_elementy.clear()
        Mixer.zastavit_zvuky()  # aby sa napr. kroky neprehrávali donekonečna

    def update(self):
        if not self.hrac:
            return

        super().update()
        Kamera.sleduj_entitu(self.hrac)

        self.kontroluj_pohyb()
        self.kontroluj_kolizie_s_nepriatelmi()
        self.kontroluj_kolizie_s_truhlami()
        self.kontroluj_kolizie_s_dvermi()

    def kontroluj_pohyb(self):
        """
        Kontroluje pohyb a kolízie všetkých entít.
        """
        # level ešte nie je úplne načítaný
        if not self.solidna_maska:
            return

        # nastavenie cielu pre všetky príšery
        # ktoré sa pohybujú priamo smerom k hráčovi
        PriamociaraPrisera.ciel = self.hrac.rect.center

        # každá entita si kontroluje pohyb a kolízie na základe
        # globálnej solídnej masky aktuálneho levelu
        for entita in self.entity:
            if isinstance(entita, Entita):
                entita.pohyb(self.solidna_maska)

    def kontroluj_kolizie_s_nepriatelmi(self):
        """
        Kontroluje kolízie hráča s nepriateľmi a berie HP.
        """

        for entita in self.entity:
            if isinstance(entita, Prisera) and self.hrac.rect.colliderect(entita.rect):
                if self.hrac.ublizit():
                    if self.hrac.zivoty <= 0:
                        self.restartovat()  # reštartovať aktuálny level
                break

    def kontroluj_kolizie_s_truhlami(self):
        """
        Kontroluje kolízie hráča s truhlami a otvára ich.
        """

        for entita in self.entity:
            if isinstance(entita, Truhla):
                zvacseny_rect = entita.rect.inflate(10, 10)
                if zvacseny_rect.colliderect(self.hrac.rect):
                    entita.otvor()
                    self.hrac.ma_kluc = True
                    self.hrac.zobraty_kluc.zobraz()
                    break

    def kontroluj_kolizie_s_dvermi(self):
        """
        Kontroluje kolízie hráča s dvermi a otvára ich, ak má hráč kľúč.
        """

        for entita in self.entity:
            if isinstance(entita, Dvere):
                zvacseny_rect = entita.rect.inflate(2, 2)
                if self.hrac.ma_kluc and zvacseny_rect.colliderect(self.hrac.rect):
                    entita.otvor()
                    self.hrac.ma_kluc = False
                    self.zmen_scenu(self.aktualny_index_sceny() + 1)
                    break

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
                    (Podlaha, DekoraciaZem),  # podlaha a dekorácie na zemy sa vykresľujú vždy prvé
                ),
                # ...inak sa kreslí podľa Y súradnice
                # pre ilúziu hĺbky
                sprite.rect.y,
            ],
        ):
            # vykreslenie sprite, s ohľadom na zoom a pozíciu kamery
            surface.blit(sprite.image, Kamera.aplikuj_na_sprite(sprite))

        # svetlo sa vykresľuje zvlášť v pôvodnom poradí,
        # tam sa nevzťahuje sortovanie Y pretože chcem aby
        # sa svetlá správne miešali s ostatnými svetlami
        for sprite in self.sprites():
            if isinstance(sprite, SvetelnaEntita):
                sprite.svetlo.aplikuj_na_tmu(tmavy_povrch)

        # vykreslenie "tmy"
        surface.blit(
            tmavy_povrch,
            (0, 0),
            # ak miešame pixel, preferujeme ten s menšou transparentnosťou
            # vďaka tomu sa "vyreže" svetlo do tmy
            # (pretože svetlo má menšiu transparentnosť ako tma, bude pri vykresľovaní preferované)
            special_flags=pygame.BLEND_RGBA_MIN,
        )

        # vykreslenie UI elementov ako posledných
        for ui_element in self.ui_elementy:
            ui_element.update()
            if isinstance(ui_element, pygame.sprite.Group):
                # ak je to group, zavoláme jej draw metódu
                # napr.: srdcia sú group, ak by to tu nebolo, neaktualizovali by sa
                ui_element.draw(surface)
            else:
                surface.blit(ui_element.image, ui_element.rect)
