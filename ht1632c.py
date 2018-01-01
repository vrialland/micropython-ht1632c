from framebuf import GS2_HMSB, FrameBuffer
from machine import Pin
from utime import sleep_us

# Colors
BLACK = const(0)
GREEN = const(1)
RED = const(2)
ORANGE = const(3)

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
    def __init__(self, width=32, height=16,
                 clk_pin=15, cs_pin=12, data_pin=14, wr_pin=13,
                 intensity=PWM_8_16):
        self._buffer = bytearray(width * height // 4)  # 2 bits per led
        self._intensity_value = intensity
        super(HT1632C, self).__init__(self._buffer, width, height, GS2_HMSB)

        self.clk = Pin(clk_pin, Pin.OUT)
        self.cs = Pin(cs_pin, Pin.OUT)
        self.data = Pin(data_pin, Pin.OUT)
        self.wr = Pin(wr_pin, Pin.OUT)

        self.begin()
        self.clear()

    def set_intensity(self, value):
        # Must be between 0 and 15
        value = min(max(0, value), 15)
        self._intensity_value = (value << 1) | 0b100101000000

        # Reinit display
        self.begin()

    def get_matrix_data(self, matrix_row, matrix_col):
        start_row = matrix_row * 8
        start_col = matrix_col * 8
        return bytearray([
            self.pixel(col, row)
            for col in range(start_col, start_col + 8)
            for row in range(start_row, start_row + 8)
        ])

    def _is_green(self, value):
        return value in (1, 3)
        # Value is either 3 (0b11) or 1 (0b01)
        #return value & 0b1

    def _is_red(self, value):
        return value in (2, 3)
        # Value is either 3 (0b11) or 2 (0b10)
        #return (value & 0b10) >> 1

    def _delay(self):
        #sleep_us(1)
        pass

    def _select_all(self):
        self.clk.off()
        self.cs.off()
        self._delay()

        self.clk.on()
        self._delay()
        self.clk.off()

        self._delay()

        self.clk.on()
        self._delay()

        self.clk.off()
        self._delay()

        self.clk.on()
        self._delay()

        self.clk.off()
        self._delay()

        self.clk.on()
        self._delay()

        self.clk.off()
        self._delay()

        self.clk.on()
        self._delay()

    def _select_none(self):
        self.clk.off()
        self.cs.on()
        self._delay()

        self.clk.on()
        self._delay()

        self.clk.off()
        self._delay()

        self.clk.on()
        self._delay()

        self.clk.off()
        self._delay()

        self.clk.on()
        self._delay()

        self.clk.off()
        self._delay()

        self.clk.on()
        self._delay()

    def _write_cmd(self, cmd):
        cmd = cmd & 0x0fff

        for i in range(12):
            j = cmd & 0x0800
            cmd = cmd << 1
            j = j >> 11
            self.wr.off()
            self.data(j)
            self._delay()

            self.wr.on()
            self._delay()

    def _write_data(self, m1, m2):
        self.wr.off()
        self.data.on()
        self._delay()

        self.wr.on()
        self._delay()

        self.wr.off()
        self.data.off()
        self._delay()

        self.wr.on()
        self._delay()

        self.wr.off()
        self.data.on()
        self._delay()

        self.wr.on()
        self._delay()

        for i in range(7):
            self.wr.off()
            self.data.off()
            self._delay()

            self.wr.on()
            self._delay()

        # Red matrix 1
        for value in m1:
            value = self._is_red(value)

            self.wr.off()
            self.data(value)
            self._delay()

            self.wr.on()
            self._delay()

        # Red matrix 2
        for value in m2:
            value = self._is_red(value)

            self.wr.off()
            self.data(value)
            self._delay()

            self.wr.on()
            self._delay()

        # Green matrix 1
        for value in m1:
            value = self._is_green(value)

            self.wr.off()
            self.data(value)
            self._delay()

            self.wr.on()
            self._delay()

        # Green matrix 2
        for value in m2:
            value = self._is_green(value)

            self.wr.off()
            self.data(value)
            self._delay()

            self.wr.on()
            self._delay()

    def begin(self):
        for cmd in (SYS_DIS,
                    COM_NMOS_8,
                    RC_MASTER_MODE,
                    SYS_EN,
                    self._intensity_value,
                    BLINK_OFF,
                    LED_ON):
            self._select_all()
            self._write_cmd(cmd)
            self._select_none()

    def clear(self):
        self._select_all()

        self.wr.off()
        self.data.on()
        self._delay()

        self.wr.on()
        self._delay()

        self.wr.off()
        self.data.off()
        self._delay()

        self.wr.on()
        self._delay()

        self.wr.off()
        self.data.on()
        self._delay()

        self.wr.on()
        self._delay()

        for i in range(7):
            self.wr.off()
            self.data.off()
            self._delay()

            self.wr.on()
            self._delay()

        for i in range(32):
            for j in range(8):
                self.wr.off()
                self.data.off()
                self._delay()

                self.wr.on()
                self._delay()

        self._select_none()

    def show(self):
        self.clk.off()
        self.cs.off()
        self._delay()

        self.clk.on()
        self._delay()
        self.clk.off()

        # HT1632 #1, ROW = 0, COL = 0 and 1
        m1 = self.get_matrix_data(0, 0)
        m2 = self.get_matrix_data(0, 1)
        self._write_data(m1, m2)

        self.cs.on()
        self._delay()

        self.clk.on()
        self._delay()
        self.clk.off()

        # HT1632 #2, ROW = 0, COL = 2 and 3
        m1 = self.get_matrix_data(0, 2)
        m2 = self.get_matrix_data(0, 3)
        self._write_data(m1, m2)

        self._delay()

        self.clk.on()
        self._delay()
        self.clk.off()

        # HT1632 #3, ROW = 1, COL = 0 and 1
        m1 = self.get_matrix_data(1, 0)
        m2 = self.get_matrix_data(1, 1)
        self._write_data(m1, m2)

        self._delay()

        self.clk.on()
        self._delay()
        self.clk.off()

        # HT1632 #4, ROW = 1, COL = 2 and 3
        m1 = self.get_matrix_data(1, 2)
        m2 = self.get_matrix_data(1, 3)
        self._write_data(m1, m2)

        self._delay()

        self.clk.on()
        self._delay()
        self.clk.off()


def test():
    h = HT1632C()
    h.text('hello', 8, 0, GREEN)
    sleep_us(1000000)
    for i in range(20):
        h.fill(BLACK)
        h.text(str(i), 0, 0, RED)
        h.show()
        sleep_us(1000000)
