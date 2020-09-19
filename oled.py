from microbit import *

cmd = [
    [0xAE],  # SSD1306_DISPLAYOFF
    [0xA4],  # SSD1306_DISPLAYALLON_RESUME
    [0xD5, 0xF0],  # SSD1306_SETDISPLAYCLOCKDIV
    [0xA8, 0x3F],  # SSD1306_SETMULTIPLEX
    [0xD3, 0x00],  # SSD1306_SETDISPLAYOFFSET
    [0 | 0x0],  # line #SSD1306_SETSTARTLINE
    [0x8D, 0x14],  # SSD1306_CHARGEPUMP
    [0x20, 0x00],  # SSD1306_MEMORYMODE
    [0x21, 0, 127],  # SSD1306_COLUMNADDR
    [0x22, 0, 63],  # SSD1306_PAGEADDR
    [0xA0 | 0x1],  # SSD1306_SEGREMAP
    [0xc8],  # SSD1306_COMSCANDEC
    [0xDA, 0x12],  # SSD1306_SETCOMPINS
    [0x81, 0xCF],  # SSD1306_SETCONTRAST
    [0xD9, 0xF1],  # SSD1306_SETPRECHARGE
    [0xDB, 0x40],  # SSD1306_SETVCOMDETECT
    [0xA6],  # SSD1306_NORMALDISPLAY
    [0xD6, 0],  # zoom set_power_off
    [0xAF]  # SSD1306_DISPLAYON
]


ADDR = 0x3C
screen = bytearray(1025)  # send byte plus pixels
screen[0] = 0x40


class OLED1306(object):
    """基本描述

    OLED1306显示屏

    """

    def __init__(self):
        for c in cmd:
            self.__command(c)

    def __command(self, c):
        i2c.write(ADDR, b'\x00' + bytearray(c))

    def __set_pos(self, col=0, page=0):
        self.__command([0xb0 | page])  # page number
        # take upper and lower value of col * 2
        c = col
        c1, c2 = c & 0x0F, c >> 4
        self.__command([0x00 | c1])  # lower start column address
        self.__command([0x10 | c2])  # upper start column address

    def set_pixel(self, x, y, color=1):
        """

        点亮或熄灭一个像素点

        Args:
            x (number): X 轴  0-127
            y (number): Y 轴  0-63
            color (number): 1 点亮 0 熄灭

        Returns:
            NONE
        """
        page, shift_page = divmod(y, 8)
        ind = x + page * 128
        b = screen[ind] | (1 << shift_page) if color else screen[ind] & ~ (1 << shift_page)
        screen[ind] = b
        self.__set_pos(x, page)
        i2c.write(ADDR, bytearray([0x40, b]))

    def set_clear(self, c=0):
        """

        删除所有显示信息，清屏

        """
        global screen
        for i in range(1, 1025):
            screen[i] = 0
        self.set_refresh()

    def set_power_on(self):
        """

        开启显示屏，默认开启

        """
        self.__command([0xAF])

    def set_power_off(self):
        """

        关闭显示屏，黑屏

        """
        self.__command([0xAE])

    def set_refresh(self):
        """

        刷新显示

        """
        self.__set_pos()
        i2c.write(ADDR, screen)

    def set_text(self, x, y, s):
        """

        显示一行文本

        Args:
            x (number): X 轴坐标 0-127
            y (number): Y 轴坐标 0-63
            s (str): 只接受字符串或字符类型参数

        Returns:
            NONE
        """
        for i in range(0, min(len(s), 12 * 2 - x)):
            for c in range(0, 5):
                col = 0
                for r in range(1, 6):
                    p = Image(s[i]).get_pixel(c, r - 1)
                    col = col | (1 << r) if (p != 0) else col
                ind = (x + i) * 5 + y * 128 + c
                screen[ind] = col
        self.__set_pos(x * 5, y)
        ind0 = x * 5 + y * 128
        i2c.write(ADDR, b'\x40' + screen[ind0:ind + 1])

    def draw_row(self, x, y, l, c=1):
        """

        画一横行

        Args:
            x (number): X 轴起始坐标 0-127
            y (number): Y 轴起始坐标 0-63
            l (number): 线段长度
            c (number): 1: 显示线段  2: 消除线段

        """
        d = 1 if l > 0 else -1
        for i in range(x, x + l, d):
            self.set_pixel(i, y, c)

    def draw_col(self, x, y, l, c=1):
        """

        画一竖列

        Args:
            x (number): X 轴起始坐标 0-127
            y (number): Y 轴起始坐标 0-63
            l (number): 线段长度
            c (number): 1: 显示线段  2: 消除线段

        """

        d = 1 if l > 0 else -1
        for i in range(y, y + l, d):
            self.set_pixel(x, i, c)


if __name__ == '__main__':
    display = OLED1306()
    display.set_clear()
    display.set_text(0, 0, "hello")