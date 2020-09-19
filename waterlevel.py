from microbit import *
from enum import *


class WATERLEVEL(object):
    """基本描述

    水位传感器，返回0-100百分比

    Args:
        RJ_pin (pin): 连接端口

    Returns:
        value: 水位百分比
    """
    def __init__(self, RJ_pin):
        if RJ_pin == J1:
            self.__pin = pin1
        elif RJ_pin == J2:
            self.__pin = pin2

    def get_waterlevel(self):
        """基本描述

        读取当前水位

        Returns:
            value: 水位百分比
        """
        __value = self.__pin.read_analog()
        value = ((__value - 0) * (100 - 0)) / (700 - 0) + 0
        return value


if __name__ == "__main__":
    s = WATERLEVEL(J1)
    while True:
        print(s.get_waterlevel())
