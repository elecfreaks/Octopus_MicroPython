from microbit import *

class LED(object):
    """基本描述

    设置LED亮度模式

    Args:
        RJ_pin (pin): 连接端口

    """

    def __init__(self, pin):
        self.__pin = pin1

    def set_led(self, state, brightness=100):
        """基本描述

        点亮或者熄灭LED

        Args:
            state (numbers): 1点亮 0熄灭
            brightness (numbers): 亮度百分比，state为1时使能 0-100

        """
        if state == 0:
            self.__pin.write_analog(0)
        elif state == 1:
            self.__pin.set_analog_period(1)
            brightness = ((brightness - 0) * (1023 - 0)) / (100 - 0) + 0;
            self.__pin.write_analog(brightness)
        else:
            print("brightness error,must 0 <= brightness <= 100")


if __name__ == "__main__":
    l = LED(pin)
    l.set_led(1, 80)
