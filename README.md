# MicroPython lib for HT1632C led matrix from Sure Electronics

This library was written to control the Sure Electronics 32x16 bicolor led
matrix from MicroPython. It has only been tested with an ESP8266 and the 32x16
bicolor matrix, using it on the 24x16 or 32x8 versions probably won't work as 
is. If you can help providing support for them, please be welcome :)


## Wiring

This is the default pin layout to control the matrix:

| ESP8266 | HT1632C | Color  | GPIO |
|---------|---------|--------|------|
| D5      | DATA    | Blue   | 14   |
| D6      | CS      | Green  | 12   |
| D7      | WR      | Yellow | 13   |
| D8      | CLK     | Orange | 15   |


This can be easily overriden using the `*_pin` params in the constructor:
```python
HT1632C(clk_pin=15, cs_pin=12, data_pin=14, wr_pin=13, intensity=PWM_10_16)
```


## Special thanks

This library is heavily inspired from these C and C++ libraries:

- https://github.com/redgick/Redgick_GFX
- https://github.com/gauravmm/HT1632-for-Arduino
- https://github.com/wildstray/ht1632c

Kudos to their authors!
