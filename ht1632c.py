from framebuf import GS2_HMSB, FrameBuffer
from machine import Pin


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