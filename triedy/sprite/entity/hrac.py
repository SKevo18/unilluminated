import typing as t

if t.TYPE_CHECKING:
    from triedy.scena import Scena

import pygame

from triedy.sprite.entity.svetelna_entita import SvetelnaEntita
from triedy.sprite.entity.fakla import Fakla
from triedy.kamera import Kamera


class Hrac(SvetelnaEntita):
    """
    Hlavná postava hry.
    """

    def __init__(self, pozicia: t.Tuple[int, int]):
        super().__init__(
            pozicia,
            (16, 16),
            self.ASSETY_ROOT / "sprite" / "hrac",
            # prevolene je animácia behu, ktorá sa iba pozastaví ak sa hráč nepohybuje:
            animacia_id="bez",
            rychlost=0.5,
        )

    def spracuj_event(self, event: pygame.event.Event, aktualna_scena: "Scena"):
        if event.type == pygame.KEYDOWN:
            # pohyb
            if event.key == pygame.K_LEFT:
                self.velocita.x = -1
                self.je_otoceny = False
            elif event.key == pygame.K_RIGHT:
                self.velocita.x = 1
                self.je_otoceny = True
            elif event.key == pygame.K_UP:
                self.velocita.y = -1
            elif event.key == pygame.K_DOWN:
                self.velocita.y = 1

            # približovanie kamery
            elif event.key == pygame.K_p:
                Kamera.zmen_priblizenie(0.5)
            elif event.key == pygame.K_o:
                Kamera.zmen_priblizenie(-0.5)

            # položenie fakle
            elif event.key == pygame.K_SPACE:
                # animácia
                self.prehrat_animaciu("poloz")

                # ak je neďaleko fakle, odobereme ju
                for fakla in aktualna_scena.sprites():
                    if isinstance(fakla, Fakla):
                        if fakla.rect.colliderect(self.rect):
                            aktualna_scena.remove(fakla)
                            break
                # inak položíme novú, zarovnanú podľa mriežky
                else:
                    podla_mriezky = (
                        (self.rect.centerx // aktualna_scena.velkost_spritu)
                        * aktualna_scena.velkost_spritu,
                        (self.rect.centery // aktualna_scena.velkost_spritu)
                        * aktualna_scena.velkost_spritu,
                    )
                    aktualna_scena.add(Fakla(podla_mriezky))

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

    def update(self):
        pohybuje_sa = self.velocita.length() > 0

        # hráčovi povolíme pohyb iba ak máme animáciu behu a nestojíme
        # napr. ak máme animáciu "poloz", tak sa hráč nemôže hýbať
        self.moze_ist = self.id_aktualnej_animacie == "bez" and pohybuje_sa

        # ak sa pohybujeme, animujeme pohyb
        # ak je animácia iná ako beh, prioritne prehrávame tú (napr. niečo položíme alebo útok a podobne)
        self.animuj = pohybuje_sa or self.id_aktualnej_animacie != "bez"
        return super().update()
