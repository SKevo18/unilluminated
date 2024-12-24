"""
Modul pre všetky sprite.
"""

from triedy.sprite.sprite import Sprite
from triedy.sprite.animovany_sprite import AnimovanySprite
from triedy.sprite.osvetleny_sprite import OsvetlenySprite

# čo sa má importovať keď použijem wildcard import
__all__ = ["Sprite", "AnimovanySprite", "OsvetlenySprite"]
