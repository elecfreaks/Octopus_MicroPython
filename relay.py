from microbit import *


class RELAY(object):
    """基本描述

    继电器

    Args:
        RJ_pin (pin): 连接端口

    """

    def __init__(self, pin):
        self.__pin = pin

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
    l = RELAY(pin1)
    l.set_laser(1)
