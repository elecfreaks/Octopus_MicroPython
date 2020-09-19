from microbit import *


class SMOKE(object):
    """基本描述

    烟雾传感器

    Args:
        RJ_pin (pin): 连接端口

    Returns:
        value: 烟雾值
    """

    def __init__(self, pin):
        self.__pin = pin

    def get_smoke(self):
        """基本描述

        获取烟雾值

        """
        return self.__pin.read_analog()


if __name__ == '__main__':
    smoke = SMOKE()
    while True:
        print(smoke.get_smoke())
