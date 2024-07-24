from microbit import *

class SOILHUMIDITY(object):
    """基本描述

    土壤湿度传感器，返回0-100百分比

    Args:
        RJ_pin (pin): 连接端口

    Returns:
        value: 水分含量百分比
    """
    def __init__(self, pin):
        self.__pin = pin

    def get_soilhumidity(self):
        """基本描述

        读取土壤含水量

        Returns:
            value: 含水量百分比
        """
        __value = self.__pin.read_analog()
        # 调整公式以使值从0开始，注意这里的计算逻辑已经修正
        value = ((__value - 0) * (100 - 0)) / (1023 - 0)
        return value


if __name__ == "__main__":
    s = SOILHUMIDITY(pin1)
    while True:
        print(s.get_soilhumidity())