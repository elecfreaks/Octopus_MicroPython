from microbit import *
import utime
import time

class DUST(object):
    """基本描述

    灰尘传感器库

    Args:
        RJ_pin (pin): 连接端口

    Returns:
        __dust: 灰尘值 ug/m3
    """

    def __init__(self, pin_vo, pin_vLED):
        self.__pin_vo = pin_vo
        self.__pin_vLED = pin_vLED

    def get_dust(self):
        """基本描述

        读取灰尘值

        Returns:
            __dust:灰尘值 ug/m3
        """
        __voltage = 0
        __dust = 0
        self.__pin_vLED.write_digital(0)
        utime.sleep_us(160)
        __voltage = self.__pin_vo.read_analog() * 6.5
        utime.sleep_us(100)
        self.__pin_vLED.write_digital(1)
        __voltage = ((__voltage - 0) * 3100) / (1023 - 0) + 0
        __dust = (__voltage - 380) * 5 / 29
        if __dust < 0:
            __dust = 0
        return __dust


if __name__ == "__main__":
    dis = DUST(pin1,pin8)
    while 1:
        print(dis.get_dust())
        sleep(500)
