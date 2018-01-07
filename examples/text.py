from ht1632c import HT1632C, GREEN, ORANGE, RED
from utils import timeit


def main():
    matrix = HT1632C()
    matrix.fill(ORANGE)
    matrix.text('abcd', 0, 0, RED)
    matrix.text('wxyz', 0, 8, GREEN)
    timeit(matrix.show)


main()