from microbit import *
from enum import *


class SOILHUMIDITY(object):
    """基本描述

    土壤湿度传感器，返回0-100百分比

    Args:
        RJ_pin (pin): 连接端口

    Returns:
        value: 水分含量百分比
    """
    def __init__(self, RJ_pin):
        if RJ_pin == J1:
            self.__pin = pin1
        elif RJ_pin == J2:
            self.__pin = pin2

    def get_soilhumidity(self):
        """基本描述

        读取土壤含水量

        Returns:
            value: 含水量百分比
        """
        __value = self.__pin.read_analog()
        value = ((__value - 0) * (100 - 0)) / (1023 - 0) + 0
        return 100-value


if __name__ == "__main__":
    s = SOILHUMIDITY(J1)
    while True:
        print(s.get_soilhumidity())
