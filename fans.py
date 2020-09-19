from microbit import *


class FANS(object):
    """基本描述

    设置风扇运动模式

    Args:
        RJ_pin (pin): 连接端口

    """

    def __init__(self, pin):
        self.__pin = pin

    def set_fans(self, state, speed=100):
        """基本描述

        点亮或者熄灭LED

        Args:
            state (numbers): 1运转 0停止
            speed (numbers): 速度百分比，state为1时使能 0-100

        """
        if state == 0:
            self.__pin.write_analog(0)
        elif state == 1:
            self.__pin.set_analog_period(1)
            speed = ((speed - 0) * (1023 - 0)) / (100 - 0) + 0;
            self.__pin.write_analog(speed)
        else:
            print("speed error,must 0 <= brightness <= 100")


if __name__ == "__main__":
    f = FANS(pin1)
    f.set_fans(1, 80)
