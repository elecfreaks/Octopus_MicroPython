from microbit import *

Start_Byte = 0x7E
Version_Byte = 0xFF
Command_Length = 0x06
End_Byte = 0xEF
Acknowledge = 0x00
CMD = 0x00
para1 = 0x00
para2 = 0x00
highByte = 0x00
lowByte = 0x00

Play = 0x0D
Stop = 0x16
PlayNext = 0x01
PlayPrevious = 0x02
Pause = 0x0E

DataBuf = [Start_Byte, Version_Byte, Command_Length, CMD, Acknowledge, para1, para2, highByte, lowByte, End_Byte]


class MP3(object):
    """基本描述

    MP3 播放器

    """

    def __init__(self, pin):
        uart.init(tx=pin)

    def __sendData(self):
        uart.write(bytes(DataBuf))
        sleep(1000)

    def __checkSum(self):
        total = 0
        for i in range(1, 7, 1):
            total += DataBuf[i]
        total = 65536 - total
        lowByte = total & 0xFF
        highByte = total >> 8
        DataBuf[7] = highByte
        DataBuf[8] = lowByte

    def exeCute(self, playType: int):
        """

        执行播放操作

        Args:
            playType (number): 操作值

        Returns:
            NONE
        """
        CMD = playType
        para1 = 0x00
        para2 = 0x00
        DataBuf[3] = CMD
        DataBuf[5] = para1
        DataBuf[6] = para2
        self.__checkSum()
        self.__sendData()

    def setVolume(self, volume: int):
        """

        设置播放器音量大小

        Args:
            volume (number): 音量值 0-30

        Returns:
            NONE
        """
        CMD = 0x06
        para1 = 0
        para2 = volume
        DataBuf[3] = CMD
        DataBuf[5] = para1
        DataBuf[6] = para2
        self.__checkSum()
        self.__sendData()

    def folderPlay(self, fileNum: int, folderNum: int = 0, Repeat: bool = False):
        """

        指定文件夹文件名播放

        Args:
            fileNum (number): 歌曲文件名
            folderNum (number): 歌曲文件夹名
            Repeat (bool): 是否重复播放

        """
        CMD = 0x0F
        para1 = folderNum
        para2 = fileNum
        DataBuf[3] = CMD
        DataBuf[5] = para2
        DataBuf[6] = para1
        self.__checkSum()
        self.__sendData()
        if Repeat:
            self.exeCute(0x19)


if __name__ == '__main__':
    player = MP3(pin1)
    while True:
        if button_a.is_pressed():
            player.exeCute(Play)
        elif button_b.is_pressed():
            player.folderPlay(1, 6, False)