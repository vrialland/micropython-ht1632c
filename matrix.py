from framebuf import GS2_HMSB, FrameBuffer
from machine import Pin


def bin2int(s):
    return int(s, base=2)


# Colors
BLACK = const(0)
GREEN = const(1)
RED = const(2)
ORANGE = const(3)

# Hardware related, data from
# https://cdn-shop.adafruit.com/datasheets/ht1632cv120.pdf

# Turn off both system oscillator and LED duty cycle generator (0000-0000-X)
SYS_DIS = const(bin2int('00000000'))
# Turn on system oscillator (0000-0001-X)
SYS_EN = const(bin2int('00000001'))
# Turn off LED duty cycle generator (0000-0010-X)
LED_OFF = const(bin2int('00000010'))
# Turn on LED duty cycle generator (0000-0011-X)
LED_ON = const(bin2int('00000011'))
# Turn off blinking function (0000-1000-X)
BLINK_OFF = const(bin2int('00001000'))
# Turn on blinking function (0000-1001-X)
BLINK_ON = const(bin2int('00001001'))
# Set slave mode and clock source from external clock, the system clock input
# from OSC pin and synchronous signal input from SYN pin (0001-0XXX-X)
SLAVE_MODE = const(bin2int('00010000'))
# Set master mode and clock source from on-chip RC oscillator, the system clock
# output to OSC pin and synchronous signal output to SYN pin (0001-10XX-X)
RC_MASTER_MODE = const(bin2int('00011000'))
# Set master mode and clock source from external clock, the system clock input
# from OSC pin and synchronous signal output to SYN pi (0001-11XX-X)
EXT_CLK_MASTER_MODE = const(bin2int('00011100'))
# Com options (0010-abXX-X)
# ab=00: N-MOS open drain output and 8 COM option
COM_N_8 = const(bin2int('00100000'))
# ab=01: N-MOS open drain output and 16 COM option
COM_N_16 = const(bin2int('00100100'))
# ab=10: P-MOS open drain output and 8 COM option
COM_P_8 = const(bin2int('00101000'))
# ab=11: P-MOS open drain output and 16 COM option
COM_P_16 = const(bin2int('00101100'))
# PWD duty
PWM_1_16 = const(bin2int('10100000'))
PWM_2_16 = const(bin2int('10100001'))
PWM_3_16 = const(bin2int('10100010'))
PWM_4_16 = const(bin2int('10100011'))
PWM_5_16 = const(bin2int('10100100'))
PWM_6_16 = const(bin2int('10100101'))
PWM_7_16 = const(bin2int('10100110'))
PWM_8_16 = const(bin2int('10100111'))
PWM_9_16 = const(bin2int('10101000'))
PWM_10_16 = const(bin2int('10101001'))
PWM_11_16 = const(bin2int('10101010'))
PWM_12_16 = const(bin2int('10101011'))
PWM_13_16 = const(bin2int('10101100'))
PWM_14_16 = const(bin2int('10101101'))
PWM_15_16 = const(bin2int('10101110'))
PWM_16_16 = const(bin2int('10101111'))


class HT1632C(FrameBuffer):
    def __init__(self, width, height, clk_pin, cs_pin, data_pin, wr_pin):
        # bytearray of width * height * 2 bits (Red/Green/Both)
        super(HT1632C, self).__init__(bytearray(width * height * 2),
                                      width, height, GS2_HMSB)
        self.clk = Pin(clk_pin, Pin.OUT)
        self.cs = Pin(cs_pin, Pin.OUT)
        self.data = Pin(data_pin, Pin.OUT)
        self.wr = Pin(wr_pin, Pin.OUT)

    def _set_master(self, pin):
        pass

    def _set_slave(self, pin):
        pass

    def flip(self):
        """Refresh display"""


screen = HT1632C(32, 16, 15, 12, 14, 13)