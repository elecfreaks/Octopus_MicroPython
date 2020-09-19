from microbit import *

TM1637_CMD1 = 64  # 0x40 data command
TM1637_CMD2 = 192  # 0xC0 address command
TM1637_CMD3 = 128  # 0x80 display control command

_SEGMENTS = (0x3F, 0x06, 0x5B, 0x4F, 0x66, 0x6D, 0x7D, 0x07, 0x7F, 0x6F, 0x77, 0x7C, 0x39, 0x5E, 0x79, 0x71)


class NIXIETUBE(object):
    """基本描述

    7段4位数码管, 7-Seg LED Nixie tube

    """

    def __init__(self, pin_clk, pin_dio, intensity=7, number=4):
        self.__clk = pin_clk
        self.__dio = pin_dio
        self.__intensity = intensity % 8
        self.__LED = number
        self.__ON = 8
        self.__buf_d = [0, 0, 0, 0]

        self.__clk.write_digital(0)
        self.__dio.write_digital(0)

        self.set_clear()

    def __start(self):
        self.__dio.write_digital(0)
        self.__clk.write_digital(0)

    def __stop(self):
        self.__dio.write_digital(0)
        self.__clk.write_digital(1)
        self.__dio.write_digital(1)

    def __write_data_cmd(self):
        self.__start()
        self.__write_byte(TM1637_CMD1)
        self.__stop()

    def __write_dsp_ctrl(self):
        self.__start()
        self.__write_byte(TM1637_CMD3 | self.__ON | self.__intensity)
        self.__stop()

    def __write_byte(self, b):
        for i in range(8):
            self.__dio.write_digital((b >> i) & 1)
            self.__clk.write_digital(1)
            self.__clk.write_digital(0)
        self.__clk.write_digital(1)
        self.__clk.write_digital(0)

    def __dat(self, bit, dat):
        self.__write_data_cmd()
        self.__start()
        self.__write_byte(TM1637_CMD2 | (bit % self.__LED))
        self.__write_byte(dat)
        self.__stop()
        self.__write_dsp_ctrl()

    def set_power_on(self):
        """

        数码管点亮显示，默认点亮


        """
        self.__ON = 8
        self.__write_data_cmd()
        self.__write_dsp_ctrl()

    def set_power_off(self):
        """

        数码管熄灭

        """
        self.__ON = 0
        self.__write_data_cmd()
        self.__write_dsp_ctrl()

    def set_intensity(self, val=None):
        """

        设置数码管显示亮度

        Args:
            val (number): 亮度 0-8

        """
        if val is None:
            return self.__intensity
        val = max(0, min(val, 8))
        if val == 0:
            self.set_power_off()
        else:
            self.__ON = 8
            self.__intensity = val - 1
            self.__write_data_cmd()
            self.__write_dsp_ctrl()

    def set_clear(self):
        """

        清空数码管显示内容

        """
        self.__dat(0, 0)
        self.__dat(1, 0)
        self.__dat(2, 0)
        self.__dat(3, 0)
        self.__buf_d = [0, 0, 0, 0]

    def set_show_bit(self, num, bit=0):
        """

        在指定位置显示单个数字

        Args:
            bit (number): 小数点位置 0-4
            num (number): 要显示的数字0-9

        """
        self.__buf_d[bit % self.__LED] = _SEGMENTS[num % 16]
        self.__dat(bit, _SEGMENTS[num % 16])

    def set_show_DP(self, bit=1, show=True):
        """

        显示一个4小数点

        Args:
            bit (number): 小数点位置 0-4
            show (bool): 显示控制位 Ture显示 False不显示

        """
        bit = bit % self.__LED
        if show:
            self.__dat(bit, self.__buf_d[bit] | 0x80)
        else:
            self.__dat(bit, self.__buf_d[bit] & 0x7F)

    def set_show_num(self, num):
        """

        显示一个4位数字

        Args:
            num (number): 要显示的数字 -999——9999

        """
        if num < 0:
            self.__dat(0, 0x40)  # '-'
            num = -num
        else:
            self.set_show_bit((num // 1000) % 10)
        self.set_show_bit(num % 10, 3)
        self.set_show_bit((num // 10) % 10, 2)
        self.set_show_bit((num // 100) % 10, 1)


if __name__ == '__main__':
    tm = NIXIETUBE(pin1, pin2)

    n = 0
    while 1:
        tm.set_show_num(n)
        n += 1
