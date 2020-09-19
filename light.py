from microbit import *


class LIGHT(object):
    """基本描述

    环境光传感器，返回lux

    Args:
        pin: 连接端口

    Returns:
        value: 光线强度 0-16000lux
    """
    def __init__(self, pin):
        self.__pin = pin

    def get_lightlevel(self):
        """基本描述

        环境光传感器，返回lux

        Returns:
            value: 光强度单位勒克司Lux
        """
        __value = self.__pin.read_analog()
        if __value <= 200:
            return ((__value - 43) * (1600 - 0)) / (200 - 43) + 0
        else:
            return ((__value - 200) * (14000 - 1600)) / (1023 - 200) + 1600


if __name__ == "__main__":
    s = LIGHT(pin1)
    while True:
        print(s.get_lightlevel())
