from microbit import *

class LASER(object):
    """基本描述

    激光发射器

    Args:
        RJ_pin (pin): 连接端口

    """

    def __init__(self, pin):
        self.__pin = pin

    def set_laser(self, state):
        """基本描述

        启动或关闭激光发射器

        Args:
            state (numbers): 1启动 0停止

        """
        if state == 0:
            self.__pin.write_digital(0)
        elif state == 1:
            self.__pin.write_digital(1)
        else:
            print("state error")


if __name__ == "__main__":
    l = LASER(pin1)
    while True:
        l.set_laser(1)
        sleep(500)
        l.set_laser(0)
        sleep(500)
