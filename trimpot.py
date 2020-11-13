from microbit import *



class TRIMPOT(object):
    """基本描述

    电位器，返回0-1023值

    Args:
        pin: 连接端口

    Returns:
        analog: 模拟值
    """
    def __init__(self, pin_d):
        self.__pin = pin_d

    def get_analog(self):
        """基本描述

        读取电位器模拟值

        Returns:
            analog: 模拟值
        """
        return self.__pin.read_analog()


if __name__ == "__main__":
    s = TRIMPOT(pin1)
    while True:
        print(s.get_analog())
