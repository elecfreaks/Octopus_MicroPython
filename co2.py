from microbit import *

class CO2(object):
    """基本描述

    二氧化碳传感器

    Args:
        pin: 连接端口

    Returns:
        value: 二氧化碳含量
    """

    def __init__(self, pin):
        self.__pin = pin

    def get_co2(self):
        """基本描述

        获取二氧化碳值

        """
        return 1024 - self.__pin.read_analog()


if __name__ == '__main__':
    co2 = CO2()
    while True:
        print(co2.get_co2())
