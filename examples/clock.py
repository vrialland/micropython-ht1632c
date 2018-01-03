import ntptime
import utime

import ht1632c


def main():
    ntptime.settime()
    matrix = ht1632c.HT1632C()
    while True:
        matrix.fill(ht1632c.BLACK)
        text = '{0:02}{1:02}'.format(*utime.localtime()[3:5])
        matrix.text(text, 0, 4, ht1632c.GREEN)
        matrix.show()
        utime.sleep_ms(10000)


main()
