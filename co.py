from microbit import *


class CO(object):
    """基本描述

    一氧化碳传感器

    Args:
        pin: 连接端口

    Returns:
        value: 一氧化碳值
    """

    def __init__(self, pin):
            self.__pin = pin

    def get_co(self):
        """基本描述

        获取一氧化碳值

        """
        return self.__pin.read_analog()


if __name__ == '__main__':
    co = CO(pin2)
    while True:
        print(co.get_co())
