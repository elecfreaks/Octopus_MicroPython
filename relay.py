from microbit import *
from enum import *


class RELAY(object):
    """基本描述

    继电器

    Args:
        RJ_pin (pin): 连接端口

    """

    def __init__(self, RJ_pin):
        if RJ_pin == J1:
            self.__pin = pin8
        elif RJ_pin == J2:
            self.__pin = pin12
        elif RJ_pin == J3:
            self.__pin = pin14
        elif RJ_pin == J4:
            self.__pin = pin16

    def set_relay(self, state):
        """基本描述

        切换继电器端子状态

        Args:
            state (numbers): 1常开闭合常闭断开 0常开常闭

        """
        if state == 0:
            self.__pin.write_digital(0)
        elif state == 1:
            self.__pin.write_digital(1)
        else:
            print("state error")


if __name__ == "__main__":
    l = RELAY(J4)
    l.set_laser(1)
