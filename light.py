from microbit import *

class LIGHT(object):
    """基本描述

    环境光传感器，返回lux

    Args:
        pin: 连接端口

    Returns:
        value: 光线强度，单位为勒克斯Lux，范围0-16000
    """
    def __init__(self, pin):
        self.__pin = pin

    def get_lightlevel(self):
        """读取环境光强度并转换为Lux单位

        Returns:
            value: 光强度，单位勒克斯Lux
        """
        raw_value = self.__pin.read_analog()

        # 为确保结果非负，我们可以直接处理不同区间的线性映射
        if raw_value <= 200:
            # 对原始区间[45, 200]进行映射到[0, 1600]
            lux = (raw_value - 45) * (1600 / (200 - 45))
        else:
            # 对原始区间[201, 1023]进行映射到[1600, 14000]
            lux = 1600 + (raw_value - 200) * ((14000 - 1600) / (1023 - 200))

        return max(0, lux)  # 确保返回值最小为0

if __name__ == "__main__":
    light_sensor = LIGHT(pin1)
    while True:
        print(light_sensor.get_lightlevel())