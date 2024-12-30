from triedy.sprity.sprite import Sprite


class Dekoracia(Sprite):
    """
    Dekorácia predstavuje sprite bez kolízie alebo interaktivity, iba dotvára prostredie levelu.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class DekoraciaZem(Sprite):
    """
    To isté ako `Dekoracia`, ale ich Y pozícia sa nemení v závislosti od toho
    ako ňou prechádzajú entity, t. j. nemá "hĺbku", je vždy na úrovni podlahy.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
