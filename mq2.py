from microbit import *



class MQ2(object):
    """基本描述

    MQ2烟雾传感器

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
    co = MQ2(pin1)
    while True:
        print(co.get_smoke())
