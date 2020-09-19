from microbit import *

DS1307_I2C_ADDRESS = 104
DS1307_REG_SECOND = 0
DS1307_REG_MINUTE = 1
DS1307_REG_HOUR = 2
DS1307_REG_WEEKDAY = 3
DS1307_REG_DAY = 4
DS1307_REG_MONTH = 5
DS1307_REG_YEAR = 6
DS1307_REG_CTRL = 7
DS1307_REG_RAM = 8


class DS1307(object):
    """基本描述

    RTC 实时时钟

    """

    # set reg
    def __i2c_setReg(self, reg, dat):
        buf = bytearray(2)
        buf[0] = reg
        buf[1] = dat
        i2c.write(DS1307_I2C_ADDRESS, buf)

    # get reg
    def __i2c_getReg(self, reg):
        buf = bytearray(1)
        buf[0] = reg
        i2c.write(DS1307_I2C_ADDRESS, buf)
        t = i2c.read(DS1307_I2C_ADDRESS, 1)
        return t[0]

    def set_start(self):
        """基本描述

        RTC 开始计时

        """
        t = self.__i2c_getReg(DS1307_REG_SECOND)
        self.__i2c_setReg(DS1307_REG_SECOND, t & 0x7F)

    def set_stop(self):
        """基本描述

        RTC 停止计时

        """
        t = self.__i2c_getReg(DS1307_REG_SECOND)
        self.__i2c_setReg(DS1307_REG_SECOND, t | 0x80)

    def __DecToHex(self, dat):
        return (dat // 10) * 16 + (dat % 10)

    def __HexToDec(self, dat):
        return (dat // 16) * 10 + (dat % 16)

    def DateTime(self, datalist=None):
        """

        设置/获取当前时间
        参数为空时读取时间，有参数为设置时间

        Args:
            datalist (list): 当前时间列表 [year,month,day,week,hour,minute,second]

        Returns:
            datalist (list): 当前时间列表 [year,month,day,week,hour,minute,second]
        """
        if datalist is None:
            i2c.write(DS1307_I2C_ADDRESS, bytearray([0]))
            buf = i2c.read(DS1307_I2C_ADDRESS, 7)
            datalist = [0] * 7
            datalist[0] = self.__HexToDec(buf[6]) + 2000
            datalist[1] = self.__HexToDec(buf[5])
            datalist[2] = self.__HexToDec(buf[4])
            datalist[3] = self.__HexToDec(buf[3])
            datalist[4] = self.__HexToDec(buf[2])
            datalist[5] = self.__HexToDec(buf[1])
            datalist[6] = self.__HexToDec(buf[0])
            return datalist
        else:
            buf = bytearray(8)
            buf[0] = 0
            buf[1] = self.__DecToHex(datalist[6] % 60)  # second
            buf[2] = self.__DecToHex(datalist[5] % 60)  # minute
            buf[3] = self.__DecToHex(datalist[4] % 24)  # hour
            buf[4] = self.__DecToHex(datalist[3] % 8)  # week day
            buf[5] = self.__DecToHex(datalist[2] % 32)  # date
            buf[6] = self.__DecToHex(datalist[1] % 13)  # month
            buf[7] = self.__DecToHex(datalist[0] % 100)  # year
            i2c.write(DS1307_I2C_ADDRESS, buf)

    def Year(self, year=None):
        """

        设置/获取当前年份
        参数为空时读取，有参数为设置

        Args:
            year (number): 当前年份

        Returns:
            year (number): 当前年份
        """
        if year == None:
            return self.__HexToDec(self.__i2c_getReg(DS1307_REG_YEAR)) + 2000
        else:
            self.__i2c_setReg(DS1307_REG_YEAR, self.__DecToHex(year % 100))

    def Month(self, month=None):
        """

        设置/获取当前月份
        参数为空时读取，有参数为设置

        Args:
            mouth (number): 当前月份

        Returns:
            mouth (number): 当前月份
        """
        if month == None:
            return self.__HexToDec(self.__i2c_getReg(DS1307_REG_MONTH))
        else:
            self.__i2c_setReg(DS1307_REG_MONTH, self.__DecToHex(month % 13))

    def Day(self, day=None):
        """

        设置/获取当前日
        参数为空时读取，有参数为设置

        Args:
            day (number): 当前日

        Returns:
            day (number): 当前日
        """
        if day == None:
            return self.__HexToDec(self.__i2c_getReg(DS1307_REG_DAY))
        else:
            self.__i2c_setReg(DS1307_REG_DAY, self.__DecToHex(day % 32))

    def Weekday(self, weekday=None):
        """

        设置/获取当前星期
        参数为空时读取，有参数为设置

        Args:
            weekday (number): 当前星期

        Returns:
            weekday (number): 当前星期
        """
        if weekday == None:
            return self.__HexToDec(self.__i2c_getReg(DS1307_REG_WEEKDAY))
        else:
            self.__i2c_setReg(DS1307_REG_WEEKDAY, self.__DecToHex(weekday % 8))

    def Hour(self, hour=None):
        """

        设置/获取当前小时
        参数为空时读取，有参数为设置

        Args:
            hour (number): 当前小时

        Returns:
            hour (number): 当前小时
        """
        if hour == None:
            return self.__HexToDec(self.__i2c_getReg(DS1307_REG_HOUR))
        else:
            self.__i2c_setReg(DS1307_REG_HOUR, self.__DecToHex(hour % 24))

    def Minute(self, minute=None):
        """

        设置/获取当前分钟
        参数为空时读取，有参数为设置

        Args:
            minute (number): 当前分钟

        Returns:
            minute (number): 当前分钟
        """
        if minute == None:
            return self.__HexToDec(self.__i2c_getReg(DS1307_REG_MINUTE))
        else:
            self.__i2c_setReg(DS1307_REG_MINUTE, self.__DecToHex(minute % 60))

    def Second(self, second=None):
        """

        设置/获取当前秒
        参数为空时读取，有参数为设置

        Args:
            second (number): 当前秒

        Returns:
            second (number): 当前秒
        """
        if second == None:
            return self.__HexToDec(self.__i2c_getReg(DS1307_REG_SECOND))
        else:
            self.__i2c_setReg(DS1307_REG_SECOND, self.__DecToHex(second % 60))


if __name__ == '__main__':
    ds = DS1307()
    ds.DateTime([2020, 5, 22, 5, 21, 32, 15])
    sleep(5000)
    print(ds.DateTime())
