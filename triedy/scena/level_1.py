from triedy.scena.scena import Scena
from triedy.sprite import OsvetlenySprite


class Level1(Scena):
    def __init__(self):
        super().__init__(OsvetlenySprite((0, 0), (100, 100), "test.png"))
