import utime

from ht1632c import HT1632C, GREEN, RED


def get_colors():
    while True:
        yield RED
        yield GREEN


def main():
    matrix = HT1632C()
    colors = get_colors()
    for d in range(8):
        matrix.rect(d, d, 32 - d * 2, 16 - d * 2, next(colors))
    matrix.show()
    while True:
        utime.sleep_ms(1000)


main()
