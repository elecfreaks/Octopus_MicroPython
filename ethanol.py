from microbit import *



class ETHANOL(object):
    """基本描述

    酒精传感器

    Args:
        RJ_pin (pin): 连接端口

    Returns:
        value: 酒精值
    """

    def __init__(self, pin):
        self.__pin = pin

    def get_ethanol(self):
        """基本描述

        获取酒精值

        """
        return self.__pin.read_analog()


if __name__ == '__main__':
    ethanol = ETHANOL(pin1)
    while True:
        print(ethanol.get_ethanol())
