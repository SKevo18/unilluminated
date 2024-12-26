from pathlib import Path

from triedy.herna_slucka import HernaSlucka

KORENOVY_ADRESAR = Path(__file__).parent

if __name__ == "__main__":
    HernaSlucka().spusti()
