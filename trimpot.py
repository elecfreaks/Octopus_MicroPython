from microbit import *
from enum import *


class TRIMPOT(object):
    """基本描述

    电位器，返回0-1023值

    Args:
        RJ_pin (pin): 连接端口

    Returns:
        analog: 模拟值
    """
    def __init__(self, RJ_pin):
        if RJ_pin == J1:
            self.__pin = pin1
        elif RJ_pin == J2:
            self.__pin = pin2

    def get_analog(self):
        """基本描述

        读取电位器模拟值

        Returns:
            analog: 模拟值
        """
        return self.__pin.read_analog()


if __name__ == "__main__":
    s = TRIMPOT(J1)
    while True:
        print(s.get_analog())
