import typing as t

import pygame.mixer

import nastavenia as n


class Mixer:
    """
    Statická trieda zodpovedná za manažment zvukov a hudby.
    """

    ROOT = n.ASSETY_ROOT / "zvuky"
    HUDBA_POZADIE = ROOT / "pozadie.mp3"
    ZVUKY: t.Dict[str, "pygame.mixer.Sound"] = {}

    zvuky_povolene = True
    hudba_povolena = True

    @staticmethod
    def nacitat_zvuky():
        """
        Načíta do pamäte všetky zvuky z priečinku zvukov.
        """

        for subor in Mixer.ROOT.iterdir():
            id = subor.stem
            Mixer.ZVUKY[id] = pygame.mixer.Sound(subor)

    @staticmethod
    def zastavit_zvuky():
        """
        Zastaví všetky zvuky ktoré sa prehrávajú.
        """

        for zvuk in Mixer.ZVUKY.values():
            zvuk.stop()

    @staticmethod
    def prehrat_zvuk(id: str) -> t.Optional[pygame.mixer.Channel]:
        """
        Prehrá určitý zvuk jedenkrát.
        """

        # ak nie sú povolené zvuky alebo sa prehráva niečo iné
        # (aby sa zvuky nemiešali)
        if not Mixer.zvuky_povolene or pygame.mixer.get_busy():
            return

        try:
            zvuk = Mixer.ZVUKY[id]
        except KeyError:
            raise ValueError(f"Zvuk s ID `{id}` neexistuje!")

        return zvuk.play()

    @staticmethod
    def prehrat_pozadie():
        """
        Začne prehrávať hudbu na pozadí
        """

        # ak nie je povolená hudba alebo sa prehráva niečo iné
        # (aby sa zvuky nemiešali)
        if not Mixer.hudba_povolena or pygame.mixer.music.get_busy():
            return

        pygame.mixer.music.load(Mixer.HUDBA_POZADIE)
        pygame.mixer.music.set_volume(0.5)
        pygame.mixer.music.play(loops=-1, fade_ms=1000)

    @staticmethod
    def stop_pozadie():
        """
        Stopne hudbu na pozadí.
        """

        pygame.mixer.music.stop()