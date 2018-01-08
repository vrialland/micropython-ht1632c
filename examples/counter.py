from time import sleep_ms

from ht1632c import BLACK, GREEN, HT1632C
from utils import timeit


def main():
    matrix = HT1632C()
    while True:
        for i in range(1, 9):
            matrix.fill(BLACK)
            x = (i - 1) % 4 * 8
            y = int(i > 4) * 8
            matrix.text(str(i), x, y, GREEN)
            timeit(matrix.show)


main()
