from microbit import *


class CRASH(object):
    """基本描述

    碰撞传感器

    Args:
        pin: 连接端口

    """

    def __init__(self, pin):
        self.__pin = pin
        self.__pin.set_pull(self.__pin.PULL_UP)

    def crash_is_pressed(self) -> bool:
        """基本描述

        碰撞传感器被按下

        Returns:
            boolean: 按下返回True, 未按下返回False

        """
        if self.__pin.read_digital() == 0:
            return True
        else:
            return False


if __name__ == '__main__':
    button = CRASH(pin1)
    while True:
        if button.crash_is_pressed():
            display.show(Image.HAPPY)
        else:
            display.show(Image.SAD)
