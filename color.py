from microbit import *

APDS9960_ADDR = 0x39

APDS9960_ENABLE = 0x80
APDS9960_ATIME = 0x81
APDS9960_CONTROL = 0x8F
APDS9960_STATUS = 0x93
APDS9960_CDATAL = 0x94
APDS9960_CDATAH = 0x95
APDS9960_RDATAL = 0x96
APDS9960_RDATAH = 0x97
APDS9960_GDATAL = 0x98
APDS9960_GDATAH = 0x99
APDS9960_BDATAL = 0x9A
APDS9960_BDATAH = 0x9B
APDS9960_GCONF4 = 0xAB
APDS9960_AICLEAR = 0xE7


class COLOR(object):
    """基本描述

    APDS9960, 颜色距离手势传感器，本文件只做颜色识别使用

    """

    def __init__(self):
        i2c.init()
        self.__initmodule()
        self.__colormode()

    def __i2cwrite_color(self, addr, reg, value):
        i2c.write(addr, bytearray([reg, value]))

    def __i2cread_color(self, addr, reg):
        i2c.write(addr, bytearray([reg]))
        t = i2c.read(addr, 1)
        return t[0]

    def __initmodule(self):
        i2c.write(APDS9960_ADDR, bytearray([APDS9960_ATIME, 252]))
        i2c.write(APDS9960_ADDR, bytearray([APDS9960_CONTROL, 0x03]))
        i2c.write(APDS9960_ADDR, bytearray([APDS9960_ENABLE, 0x00]))
        i2c.write(APDS9960_ADDR, bytearray([APDS9960_GCONF4, 0x00]))
        i2c.write(APDS9960_ADDR, bytearray([APDS9960_AICLEAR, 0x00]))
        i2c.write(APDS9960_ADDR, bytearray([APDS9960_ENABLE, 0x01]))

    def __colormode(self):
        tmp = self.__i2cread_color(APDS9960_ADDR, APDS9960_ENABLE) | 0x2
        self.__i2cwrite_color(APDS9960_ADDR, APDS9960_ENABLE, tmp)

    def __rgbtohsl(self, color_r, color_g, color_b):
        __hue = 0
        __R = color_r * 100 / 255
        __G = color_g * 100 / 255
        __B = color_b * 100 / 255
        # 取最大值
        __maxVal = max(__R, max(__G, __B))
        __minVal = min(__R, min(__G, __B))
        '''
        if __R < __G and __B < __G:
            __maxVal = __G
        elif __R < __B and __G < __B:
            __maxVal = __B
        else:
            __maxVal = __R
        # 取最小值
        if __R > __G and __B > __G:
            __minVal = __G
        elif __R > __B and __G > __B:
            __minVal = __B
        else:
            __minVal = __R
        '''
        __delta = __maxVal - __minVal

        if __delta <= 0:
            __hue = 0

        elif __maxVal == __R and __G >= __B:
            __hue = (60 * ((__G - __B) * 100 / __delta)) / 100

        elif __maxVal == __R and __G < __B:
            __hue = (60 * ((__G - __B) * 100 / __delta) + 360 * 100) / 100

        elif __maxVal == __G:
            __hue = (60 * ((__B - __R) * 100 / __delta) + 120 * 100) / 100

        elif __maxVal == __B:
            __hue = (60 * ((__R - __G) * 100 / __delta) + 240 * 100) / 100

        return __hue

    def get_hue(self):
        """

        读取当前颜色HUE值

        Returns:
            hue HUE颜色系统中的颜色，根据色环判断具体颜色
        """
        __tmp = self.__i2cread_color(APDS9960_ADDR,
                                     APDS9960_STATUS) & 0x1
        while not __tmp:
            sleep(1)
            __tmp = self.__i2cread_color(APDS9960_ADDR,
                                         APDS9960_STATUS) & 0x1

        c = self.__i2cread_color(APDS9960_ADDR, APDS9960_CDATAL) + \
            self.__i2cread_color(APDS9960_ADDR, APDS9960_CDATAH) * 256
        r = self.__i2cread_color(APDS9960_ADDR, APDS9960_RDATAL) + \
            self.__i2cread_color(APDS9960_ADDR, APDS9960_RDATAH) * 256
        g = self.__i2cread_color(APDS9960_ADDR, APDS9960_GDATAL) + \
            self.__i2cread_color(APDS9960_ADDR, APDS9960_GDATAH) * 256
        b = self.__i2cread_color(APDS9960_ADDR, APDS9960_BDATAL) + \
            self.__i2cread_color(APDS9960_ADDR, APDS9960_BDATAH) * 256

        avg = c / 3
        r = r * 255 / avg
        g = g * 255 / avg
        b = b * 255 / avg
        hue = self.__rgbtohsl(r, g, b)
        return hue


if __name__ == '__main__':
    color = COLOR()
    while True:
        print("HUE: ", color.get_hue())
        sleep(5)
