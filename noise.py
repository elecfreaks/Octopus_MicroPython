from microbit import *


class NOISE:
    """基本描述

    环境噪声传感器，返回值是噪声分贝值

    Args:
        RJ_pin (pin): 连接端口

    Returns:
        noise: 分贝值
    """
    def __init__(self, pin):
        self.pin = pin

    def get_noise(self):
        """基本描述

        读取噪声值

        Returns:
            noise: 分贝值
        """
        level, tl, h, sum_l, sum_h = 0, 0, 0, 0, 0
        for i in range(0, 1000):
            level = level + self.pin.read_analog()
            self.pin.read_analog()
        level = level / 1000
        for i in range(0, 1000):
            voltage = self.pin.read_analog()
            if voltage >= level:
                h += 1
                sum_h = sum_h + voltage
            else:
                tl += 1
                sum_l = sum_l + voltage
        if h == 0:
            sum_h = level
        else:
            sum_h = sum_h / h
        if tl == 0:
            sum_l = level
        else:
            sum_l = sum_l / tl
        noise = sum_h - sum_l
        if noise <= 4:
            noise = ((noise - 0) * (50 - 30)) / (4 - 0) + 30
        elif noise <= 8:
            noise = ((noise - 4) * (55 - 50)) / (8 - 4) + 50
        elif noise <= 14:
            noise = ((noise - 9) * (60 - 55)) / (14 - 9) + 55
        elif noise <= 32:
            noise = ((noise - 15) * (70 - 60)) / (32 - 15) + 60
        elif noise <= 60:
            noise = ((noise - 33) * (75 - 70)) / (60 - 33) + 70
        elif noise <= 100:
            noise = ((noise - 61) * (80 - 75)) / (100 - 61) + 75
        elif noise <= 150:
            noise = ((noise - 101) * (85 - 80)) / (150 - 101) + 80
        elif noise <= 231:
            noise = ((noise - 151) * (90 - 85)) / (231 - 150) + 85
        else:
            noise = ((noise - 231) * (120 - 90)) / (1023 - 231) + 90
        return noise


if __name__ == "__main__":
    s = NOISE(pin1)
    while True:
        x = s.get_noise()
        print(x)
        sleep(200)
