from microbit import *
from enum import *


class UVLEVEL(object):
    """基本描述

    紫外线强度传感器

    Args:
        RJ_pin (pin): 连接端口

    Returns:
        value: 紫外线强度值 0-15
    """
    def __init__(self, RJ_pin):
        if RJ_pin == J1:
            self.__pin = pin1
        elif RJ_pin == J2:
            self.__pin = pin2

    def get_uvlevel(self):
        """基本描述

        读取当前紫外线值

        Returns:
            value: 紫外线强度值 0-15
        """
        __value = self.__pin.read_analog()
        value = ((__value - 0) * (15 - 0)) / (625 - 0) + 0
        return value


if __name__ == "__main__":
    s = UVLEVEL(J1)
    while True:
        print(s.get_uvlevel())
