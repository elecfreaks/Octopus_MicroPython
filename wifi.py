from microbit import *
from enum import *


class WIFI(object):
    """基本描述

    ESP8266 WI-FI模块AT固件

    """

    __topic_def = ""
    __userToken_def = 0

    def __init__(self, RJ_pin):
        if RJ_pin == J1:
            uart.init(tx=pin8, rx=pin1, baudrate=115200)
        elif RJ_pin == J2:
            uart.init(tx=pin12, rx=pin8, baudrate=115200)
        elif RJ_pin == J3:
            uart.init(tx=pin14, rx=pin13, baudrate=115200)
        elif RJ_pin == J4:
            uart.init(tx=pin16, rx=pin15, baudrate=115200)
        uart.write("AT+RESTORE" + "\r\n")
        sleep(100)
        uart.write("AT+CWMODE=1" + "\r\n")

    def __sendData(self, CMD):
        uart.write(CMD + "\r\n")
        time = running_time()
        uart_read_str = ""
        while True:
            uart_read_str += str(uart.read())
            if "OK" in uart_read_str:
                return True
            if running_time() - time > 5000:
                return False
            if len(uart_read_str) > 100:
                uart_read_str = ""

    def connectWIFI(self, SSID, password):
        """

        连接WI-FI，只支持2.4G网络

        Args:
            SSID (string): WI-FI名称
            password (string): WI-FI密码

        Returns:
            boolean: 执行是否成功
        """
        first_CMD = "AT+CWJAP=" + "\"" + SSID + "\",\"" + password + "\"\r\n"
        return self.__sendData(first_CMD)

    def connectThingSpeak(self):
        """

        连接ThingSpeak,必须连接才能上传数据, 上传后会自动断连接


        Returns:
            boolean: 执行是否成功
        """
        first_CMD = "AT+CIPSTART=\"TCP\",\"api.thingspeak.com\",80"
        return self.__sendData(first_CMD)

    def upDataToThingSpeak(self, write_api_key: str, n1: int = 0, n2: int = 0, n3: int = 0, n4: int = 0, n5: int = 0,
                           n6: int = 0, n7: int = 0, n8: int = 0):
        """

        设置要上传的数据并上传

        Args:
            write_api_key (string): ThingSpeak的写入API
            n1 (number): 1通道数据
            n2 (number): 2通道数据
            n3 (number): 3通道数据
            n4 (number): 4通道数据
            n5 (number): 5通道数据
            n6 (number): 6通道数据
            n7 (number): 7通道数据
            n8 (number): 8通道数据

        Returns:
            boolean: 执行是否成功
        """
        toSendCMD = "GET /update?api_key=" + write_api_key + "&field1=" + n1 + "&field2=" + n2 + "&field3=" + n3 + \
                    "&field4=" + n4 + "&field5= " + n5 + "&field6=" + n6 + "&field7=" + n7 + "&field8=" + n8
        uart.write("AT+CIPSEND=" + (len(toSendCMD) + 2) + "\r\n")
        sleep(100)
        return self.__sendData(toSendCMD)

    ##############################kidsiot##########################
    def connectKidsiot(self, userToken, Topic):
        """

        连接Kidsiot

        Args:
            userToken (string): 用户唯一识别码
            Topic (number): 设备唯一识别码

        Returns:
            boolean: 执行是否成功
        """
        self.__topic_def = Topic
        self.__userToken_def = userToken
        self.__sendData("AT+CIPSTART=\"TCP\",\"139.159.161.57\",5555")
        text_one = "{\"topic\":\"" + Topic + "\",\"userToken\":\"" + userToken + "\",\"op\":\"init\"}"
        uart.write("AT+CIPSEND=" + (len(text_one) + 2) + "\r\n")
        sleep(100)
        self.__sendData(text_one)

    def uploadKidsiot(self, data: int):
        """

        上传数据到kidsiot

        Args:
            data (number): 数据

        Returns:
            boolean: 执行是否成功
        """
        text_one = "{\"topic\":\"" + self.__topic_def + "\",\"userToken\":\"" + self.__userToken_def + \
                   "\",\"op\":\"up\",\"data\":\"" + data + "\"}"
        uart.write("AT+CIPSEND=" + (len(text_one) + 2) + "\r\n")
        sleep(100)
        return self.__sendData(text_one)

    def disconnectKidsiot(self):
        """

        断开与kidsiot的连接

        Returns:
            boolean: 执行是否成功
        """
        text_one = "{\"topic\":\"" + self.__topic_def + "\",\"userToken\":\"" + self.__userToken_def + \
                   "\",\"op\":\"close\"}"
        uart.write("AT+CIPSEND=" + (len(text_one) + 2) + "\r\n")
        sleep(100)
        return self.__sendData(text_one)

    def kidsiotSwitch(self):
        """

        Kidsiot开关功能


        Returns:
            string: switchon: 打开
            string: switchoff: 关闭
            string: none: 无操作
        """
        uart_read_str = ""
        uart_read_str += str(uart.read())
        if "switchon" in uart_read_str:
            return "switchon"
        elif "switchoff" in uart_read_str:
            return "switchoff"
        else:
            return "None"


if __name__ == '__main__':
    IoT = WIFI(J1)
    while True:
        if button_a.is_pressed():
            print(IoT.connectWIFI("ELECFREAKS_2.4G", "elecfreaks2019"))
        elif button_b.is_pressed():
            IoT.connectThingSpeak()
