import typing as t

import pygame
import pygame_widgets.button

class Tlacidlo(pygame_widgets.button.Button):
    def __init__(self, okno: pygame.Surface, pozicia: tuple[int, int],  text: str, po_kliknuti: t.Callable):
        super().__init__(
            okno, pozicia[0], pozicia[1], 300, 150, text=text,
            fontSize=50, margin=20,
            inactiveColour=(255, 0, 0),
            pressedColour=(0, 255, 0), radius=20,
            onClick=po_kliknuti
        )
