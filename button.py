from microbit import *


class BUTTON(object):
    """基本描述

    单个按钮

    Args:
        pin: 连接端口

    """

    def __init__(self, pin):
        self.__pin = pin
        self.__pin.set_pull(self.__pin.PULL_UP)

    def Is_pressed(self) -> bool:
        """基本描述

        判断按钮按下

        Returns:
            boolean: 按下返回True, 未按下返回False

        """
        if self.__pin.read_digital() == 0 and self.__pin.read_digital() == 1:
            return True
        else:
            return False


if __name__ == '__main__':
    button = BUTTON(pin1)
    while True:
        if button.Is_pressed():
            display.show(Image.HAPPY)
        else:
            display.clear()