import typing as t

if t.TYPE_CHECKING:
    from triedy.sceny.scena import Scena

import pygame

import nastavenia as n
from triedy.kamera import Kamera
from triedy.mixer import Mixer
from triedy.sprity.entity.fakla import Fakla
from triedy.sprity.entity.svetelna_entita import SvetelnaEntita
from triedy.ui.fakle_pocitadlo import FaklePocitadlo
from triedy.ui.srdcia_pocitadlo import SrdciaPocitadlo
from triedy.ui.zobraty_kluc import ZobratyKluc


class Hrac(SvetelnaEntita):
    """
    Hlavná postava hry.
    """

    def __init__(self, pozicia: t.Tuple[int, int]):
        super().__init__(
            pozicia,
            n.ASSETY_ROOT / "sprite" / "hrac",
            # prevolene je animácia behu, ktorá sa iba pozastaví ak sa hráč nepohybuje:
            animacia_id="bez",
            rychlost=1.0,
        )

        self.ma_kluc = False
        """Či má hráč kľúč na odomknutie dverí do ďalšieho levelu."""
        self.zivoty = 3
        """Zdravie hráča."""
        self.cas_nesmrtelnosti = 0
        """Odpočítava sa každý frame, ak je viac ako 1, hráč nemôže stratiť život."""
        self.aktualny_zvuk_krokov = None
        """Zvuk krokov, ktorý sa momentálne prehráva (ak prestaneme chodiť, zastavíme aj tento zvuk)"""

        self.pocitadlo_zivotov = SrdciaPocitadlo((10, 10), pocet_srdc=3)
        """Objekt pre zobrazenie životov. Predvolene 3 - mení sa iba vtedy, ak sa hráč zraní."""
        self.pocitadlo_fakli = FaklePocitadlo((10, 32))
        """Objekt pre zobrazovanie počtu faklí."""
        self.zobraty_kluc = ZobratyKluc()
        """Zobrazí sa, ak hráč zoberie kľúč."""

    def spracuj_event(self, event: pygame.event.Event, aktualna_scena: "Scena"):
        if event.type == pygame.KEYDOWN:
            # pohyb
            if event.key == pygame.K_LEFT:
                self.velocita.x = -1 * self.rychlost
                self.je_otoceny = False
            elif event.key == pygame.K_RIGHT:
                self.velocita.x = 1 * self.rychlost
                self.je_otoceny = True
            elif event.key == pygame.K_UP:
                self.velocita.y = -1 * self.rychlost
            elif event.key == pygame.K_DOWN:
                self.velocita.y = 1 * self.rychlost

            # približovanie kamery
            elif event.key == pygame.K_p:
                Kamera.zmen_priblizenie(0.5)
            elif event.key == pygame.K_o:
                Kamera.zmen_priblizenie(-0.5)

            # položenie fakle
            elif event.key == pygame.K_SPACE:
                # nemôžme položiť faklu, ak pokladáme alebo berieme inú
                if self.id_aktualnej_animacie == "poloz":
                    return

                # ak je neďaleko fakľa, odobereme ju
                for sprite in aktualna_scena.sprites():
                    if isinstance(sprite, Fakla) and sprite.rect.colliderect(self.rect):
                        aktualna_scena.remove(sprite)
                        self.pocitadlo_fakli.pocet_fakli += 1
                        break

                # nie sme neďaleko žiadnej fakle - položíme novú, zarovnanú podľa mriežky:
                else:
                    if self.pocitadlo_fakli.pocet_fakli <= 0:
                        return  # nepokračujeme ďalej, aby sa neprehral ani zvuk na konci

                    podla_mriezky = (
                        (self.rect.centerx // aktualna_scena.velkost_spritu)
                        * aktualna_scena.velkost_spritu,
                        (self.rect.centery // aktualna_scena.velkost_spritu)
                        * aktualna_scena.velkost_spritu,
                    )
                    aktualna_scena.add(Fakla(podla_mriezky))
                    self.pocitadlo_fakli.pocet_fakli -= 1

                # animácia a zvuk
                Mixer.prehrat_zvuk("poloz")
                self.prehrat_animaciu("poloz")

        elif event.type == pygame.KEYUP:
            # pohyb - zastavíme, iba ak sme sa pohybovali tým smerom
            # (aby sa hráč nezastavil ak zmení smer na opačný)
            if event.key == pygame.K_LEFT and self.velocita.x < 0:
                self.velocita.x = 0
            elif event.key == pygame.K_RIGHT and self.velocita.x > 0:
                self.velocita.x = 0
            elif event.key == pygame.K_UP and self.velocita.y < 0:
                self.velocita.y = 0
            elif event.key == pygame.K_DOWN and self.velocita.y > 0:
                self.velocita.y = 0

    def ublizit(self) -> bool:
        """
        Odoberie hráčovi jeden život a nastaví čas nesmrtelnosti na 40.

        Ak vráti `True`, znamená to že hráč sa úspešne zranil (t. j. nebol nesmrteľný).
        """

        if self.cas_nesmrtelnosti > 0:
            return False

        self.cas_nesmrtelnosti = 40
        self.svetlo.farba = (255, 100, 0)  # aby sme vedeli že hráč sa zranil
        self.zivoty -= 1
        self.pocitadlo_zivotov.pocet_srdc = self.zivoty
        Mixer.prehrat_zvuk("ublizenie")

        return True

    def update(self):
        # odoberieme čas nesmrtelnosti
        if self.cas_nesmrtelnosti > 0:
            self.cas_nesmrtelnosti -= 1
        else:
            # hráč sa už môže zraniť, resetujeme svetlo
            self.svetlo.farba = (255, 255, 255)

        pohybuje_sa = self.velocita.length() > 0

        # hráčovi povolíme pohyb iba ak máme animáciu behu a nestojíme
        # napr. ak máme animáciu "poloz", tak sa hráč nemôže hýbať
        self.moze_ist = self.id_aktualnej_animacie == "bez" and pohybuje_sa

        if self.moze_ist:
            if not self.aktualny_zvuk_krokov:
                self.aktualny_zvuk_krokov = Mixer.prehrat_zvuk("kroky")
        elif self.aktualny_zvuk_krokov:
            self.aktualny_zvuk_krokov.stop()
            self.aktualny_zvuk_krokov = None

        # ak sa pohybujeme, animujeme pohyb
        # ak je animácia iná ako beh, prioritne prehrávame tú (napr. niečo položíme alebo útok a podobne)
        self.animuj = pohybuje_sa or self.id_aktualnej_animacie != "bez"

        return super().update()
