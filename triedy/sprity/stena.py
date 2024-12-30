from triedy.sprity.sprite import Sprite


class Stena(Sprite):
    """
    Stena predstavuje solidný objekt, cez ktorý nemôžu entity prechádzať.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
