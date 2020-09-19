from microbit import *
from enum import *


class PM25(object):
    """基本描述

    PM 2.5传感器

    Args:
        RJ_pin (pin): 连接端口

    Returns:
        value: PM2.5值（微克/立方米）
    """

    def __init__(self, RJ_pin):
        if RJ_pin == J1:
            self.__pin = pin8
        elif RJ_pin == J2:
            self.__pin = pin12
        elif RJ_pin == J3:
            self.__pin = pin14
        elif RJ_pin == J4:
            self.__pin = pin16

    def get_pm25(self):
        """基本描述

        获取PM2.5值

        """
        while self.__pin.read_digital() != 0:
            pass
        while self.__pin.read_digital() != 1:
            pass
        pm25 = running_time()
        while self.__pin.read_digital() != 0:
            pass
        pm25 = running_time() - pm25
        return pm25


if __name__ == '__main__':
    pm2_5 = PM25(J1)
    while True:
        print(pm2_5.get_pm25())
        sleep(1000)

