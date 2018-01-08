from framebuf import GS2_HMSB, FrameBuffer
from machine import Pin
import micropython

# Colors
BLACK = const(0)
GREEN = const(2)
RED = const(1)
ORANGE = const(3)

# Chip selection
SELECT_NONE = const(-2)
SELECT_ALL = const(-1)
NB_CHIPS = const(4)

# Display infos
WIDTH = const(32)
HEIGHT = const(16)

# Hardware related, data from
# https://cdn-shop.adafruit.com/datasheets/ht1632cv120.pdf

# Turn off both system oscillator and LED duty cycle generator (0000-0000-X)
SYS_DIS = const(0b100000000000)
# Turn on system oscillator (0000-0001-X)
SYS_EN = const(0b100000000010)
# Turn off LED duty cycle generator (0000-0010-X)
LED_OFF = const(0b100000000100)
# Turn on LED duty cycle generator (0000-0011-X)
LED_ON = const(0b100000000110)
# Turn off blinking function (0000-1000-X)
BLINK_OFF = const(0b100000010000)
# Turn on blinking function (0000-1001-X)
BLINK_ON = const(0b100000010010)
# Set slave mode and clock source from external clock, the system clock input
# from OSC pin and synchronous signal input from SYN pin (0001-0XXX-X)
SLAVE_MODE = const(0b100000100000)
# Set master mode and clock source from on-chip RC oscillator, the system clock
# output to OSC pin and synchronous signal output to SYN pin (0001-10XX-X)
RC_MASTER_MODE = const(0b100000110000)
# Set master mode and clock source from external clock, the system clock input
# from OSC pin and synchronous signal output to SYN pi (0001-11XX-X)
EXT_CLK_MASTER_MODE = const(0b100000111000)
# Com options (0010-abXX-X)
# ab=00: N-MOS open drain output and 8 COM option
COM_NMOS_8 = const(0b100001000000)
# ab=01: N-MOS open drain output and 16 COM option
COM_NMOS_16 = const(0b100001001000)
# ab=10: P-MOS open drain output and 8 COM option
COM_PMOS_8 = const(0b100001010000)
# ab=11: P-MOS open drain output and 16 COM option
COM_PMOS_16 = const(0b100001011000)
# PWD duty
PWM_1_16 = const(0b100101000000)
PWM_2_16 = const(0b100101000010)
PWM_3_16 = const(0b100101000100)
PWM_4_16 = const(0b100101000110)
PWM_5_16 = const(0b100101001000)
PWM_6_16 = const(0b100101001010)
PWM_7_16 = const(0b100101001100)
PWM_8_16 = const(0b100101001110)
PWM_9_16 = const(0b100101010000)
PWM_10_16 = const(0b100101010010)
PWM_11_16 = const(0b100101010100)
PWM_12_16 = const(0b100101010110)
PWM_13_16 = const(0b100101011000)
PWM_14_16 = const(0b100101011010)
PWM_15_16 = const(0b100101011100)
PWM_16_16 = const(0b100101011110)


class HT1632C(FrameBuffer):
    def __init__(self, clk_pin=15, cs_pin=12, data_pin=14, wr_pin=13,
                 intensity=PWM_10_16):
        self._buffer = bytearray(WIDTH * HEIGHT // 4)  # 2 bits per led
        self._intensity_value = intensity
        super(HT1632C, self).__init__(self._buffer, WIDTH, HEIGHT, GS2_HMSB)

        self.clk = Pin(clk_pin, Pin.OUT)
        self.cs = Pin(cs_pin, Pin.OUT, value=1)
        self.data = Pin(data_pin, Pin.OUT)
        self.wr = Pin(wr_pin, Pin.OUT)

        self.begin()
        self.show()

    def pulse_clk(self):
        self.clk(1)
        self.clk(0)

    def set_intensity(self, value):
        # Must be between 0 and 15
        value = min(max(0, value), 15)
        self._intensity_value = (value << 1) | 0b100101000000

        # Reinit display
        self.begin()

    def get_ht1632_data(self, matrix_row, matrix_col):
        """Get data associated to an HT1632 chip"""
        start_row = matrix_row * 8
        stop_row = start_row + 8
        start_col = matrix_col * 16
        stop_col = start_col + 16
        return [
            self.pixel(col, row)
            for col in range(start_col, stop_col)
            for row in range(start_row, stop_row)
        ]

    def is_green(self, value):
        """Bitwise test if value is ORANGE (0b11) or GREEN (0b01)"""
        return value & 0b1

    def is_red(self, value):
        """Bitwise test if value is ORANGE (0b11) or RED (0b10)"""
        return (value & 0b10) >> 1

    def _select(self, chip):
        if chip in (SELECT_NONE, SELECT_ALL):
            value = 1 if chip == SELECT_NONE else 0
            self.cs(value)
            for idx in range(NB_CHIPS):
                self.pulse_clk()
        else:
            self._select(SELECT_NONE)
            self.cs(0)
            self.pulse_clk()
            self.cs(1)
            for idx in range(chip):
                self.pulse_clk()

    def _write_cmd(self, cmd):
        """Write a command, one bit at a time"""
        cmd = cmd & 0x0fff
        for i in range(12):
            j = cmd & 0x0800
            cmd = cmd << 1
            j = j >> 11
            self.wr(0)
            self.data(j)
            self.wr(1)

    @micropython.native
    def _write_data(self, red, green):
        """Write a part of the framebuffer data to the selected chip"""

        # Write WR command
        for data in (1, 0, 1):
            self.wr(0)
            self.data(data)
            self.wr(1)

        # Send address (0 as we're writing sequentially)
        for i in range(7):
            self.wr(0)
            self.data(0)
            self.wr(1)

        # Red layer
        for value in red:
            self.wr(0)
            self.data(value)
            self.wr(1)

        # Green layer
        for value in green:
            self.wr(0)
            self.data(value)
            self.wr(1)

    def begin(self):
        """Initialize hardware"""
        for cmd in (SYS_DIS,
                    COM_NMOS_8,
                    RC_MASTER_MODE,
                    SYS_EN,
                    self._intensity_value,
                    BLINK_OFF,
                    LED_ON):
            self._select(SELECT_ALL)
            self._write_cmd(cmd)
            self._select(SELECT_NONE)

    def show(self):
        """Display framebuffer data on hardware"""
        self._select(SELECT_ALL)
        self._write_cmd(SYS_EN)
        self._select(SELECT_NONE)

        for chip in range(NB_CHIPS):
            self._select(chip)

            row = 0 if chip in (0, 1) else 1
            col = 0 if chip in (0, 2) else 1

            data = self.get_ht1632_data(row, col)
            red = (self.is_red(value) for value in data)
            green = (self.is_green(value) for value in data)
            self._write_data(red, green)

            self._select(SELECT_NONE)