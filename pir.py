from microbit import *


class PIR(object):
    """基本描述

    人体红外检测, 运动检测

    Args:
        RJ_pin (pin): 连接端口

    """

    def __init__(self, pin):
        self.__pin = pin


    def PIR_is_decection(self) -> bool:
        """基本描述

        检测到人体或者运动

        Returns:
            boolean: 检测到返回True, 未检测返回False

        """
        if self.__pin.read_digital():
            return True
        else:
            return False


if __name__ == '__main__':
    sensor = PIR(pin1)
    while True:
        if sensor.PIR_is_decection():
            display.show(Image.HAPPY)
        else:
            display.show(Image.SAD)
