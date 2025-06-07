from microbit import *
import time

#WIFI模块
#注：因文件大小编译限制，当因文件过大无法下载时，可删除未用到的类平台，例如将class ESP8266_IFTTT整体直接删除
class ESP8266_IoT:
    J1 = 0
    J2 = 1
    J3 = 2
    J4 = 3
    wifi_init_flag = True
    def __init__(self, *ports, tx=None, rx=None):
        """
        初始化 ESP8266 模块。
        Args:
            *ports: 可选，一个整数，表示 J1-J4 中的端口号。
            tx (microbit.pin): 自定义发送引脚
            rx (microbit.pin): 自定义接收引脚
            eg:IoT = ESP8266_IoT(ESP8266_IoT.J1) or IoT = ESP8266_IoT(tx = pin8,rx = pin1)
        """
        self.wifi_connected = False
        self.msg_handler_map = {}
        self.str_buf = ""

        # 判断是否使用预设配置（J1-J4）
        if ports:
            port = ports[0]
            if port == ESP8266_IoT.J1:
                tx_pin, rx_pin = pin8, pin1
            elif port == ESP8266_IoT.J2:
                tx_pin, rx_pin = pin12, pin2
            elif port == ESP8266_IoT.J3:
                tx_pin, rx_pin = pin14, pin13
            elif port == ESP8266_IoT.J4:
                tx_pin, rx_pin = pin16, pin15
            else:
                raise ValueError("无效的端口号，请使用 J1-J4")
        elif tx is not None and rx is not None:
            tx_pin, rx_pin = tx, rx
        else:
            raise ValueError("必须提供 J1-J4 或自定义 tx/rx 引脚")

        if ESP8266_IoT.wifi_init_flag:
            uart.init(baudrate=115200, tx=tx_pin, rx=rx_pin)
            run_every(self.serial_data_handler, ms=2)
            ESP8266_IoT.wifi_init_flag = False

    def serial_data_handler(self):
        try:
            if uart.any():
                data = uart.read()
                if data is not None:
                    self.str_buf += data.decode('utf-8')
        except Exception as e:
            return

        splits = self.str_buf.split('\n')
        if self.str_buf and self.str_buf[-1] != '\n':
            self.str_buf = splits.pop()
        else:
            self.str_buf = ""
        for res in splits:
            for key in self.msg_handler_map:
                if key in res:
                    handler_info = self.msg_handler_map[key]
                    if handler_info['type'] == 0:
                        handler_info['handler'](res)
                    elif handler_info['type'] == 1:
                        handler_info['msg'] = res

    def send_at(self, command, wait=0):
        uart.write((command + '\r\n').encode())
        if wait > 0:
            time.sleep_ms(wait)

    def register_msg_handler(self, key, handler):
        self.msg_handler_map[key] = {
            'type': 0,
            'handler': handler
        }

    def remove_msg_handler(self, key):
        if key in self.msg_handler_map:
            del self.msg_handler_map[key]

    def wait_for_response(self, key, wait=1000):
        start_time = time.ticks_ms()
        self.msg_handler_map[key] = {
            'type': 1,
            'msg': None
        }

        while time.ticks_diff(time.ticks_ms(), start_time) < wait:
            sleep(5)
            if key not in self.msg_handler_map:
                return None
            if self.msg_handler_map[key].get('msg') is not None:
                res = self.msg_handler_map[key]['msg']
                del self.msg_handler_map[key]
                return res
        del self.msg_handler_map[key]
        return None

    def send_request(self, command, key, wait=1000):
        uart.write((command + '\r\n').encode())
        return self.wait_for_response(key, wait)

    def reset_esp8266(self):
        self.send_request("AT+RESTORE", "ready")
        self.send_request("AT+RST", "ready", 2000)
        if self.send_request("AT+CWMODE=1", "OK") is None:
            self.send_request("AT+CWMODE=1", "OK")
        self.send_request(
            'AT+CIPSNTPCFG=1,8,"ntp1.aliyun.com","0.pool.ntp.org","time.google.com"',
            "OK", 3000
        )

    def connect_wifi(self, ssid, password):
        self.register_msg_handler("WIFI DISCONNECT", lambda str: setattr(self, 'wifi_connected', False))
        self.register_msg_handler("WIFI GOT IP", lambda str: setattr(self, 'wifi_connected', True))

        retry_count = 2
        while True:
            self.send_at('AT+CWJAP="{0}","{1}"'.format(ssid, password))
            start = time.ticks_ms()
            while time.ticks_diff(time.ticks_ms(), start) < 7000:
                sleep(100)
                if self.wifi_connected:
                    return
            if not self.wifi_connected and retry_count > 0:
                retry_count -= 1
                self.reset_esp8266()
            else:
                break

    def wifi_state(self):
        return self.wifi_connected

    def init_wifi(self):
        self.reset_esp8266()

#MQTT模块
class ESP8266_MQTT:
    def __init__(self, iot_instance):
        """
        初始化 MQTT 模块
        """
        self.iot = iot_instance
        # MQTT 状态
        self.mqtt_connected = False
        self.mqtt_sub_handlers = {}  
        self.mqtt_sub_qos = {}       

    def set_mqtt_config(self, scheme: int, client_id: str, username: str, password: str, path: str):
        """
        设置 MQTT 客户端配置

        Args:
            scheme: 1=TCP, 2=TLS
            client_id: 客户端 ID
            username: 用户名
            password: 密码
            path: 路径
        """
        self.iot.send_at('AT+MQTTUSERCFG=0,{},"{}","{}","{}",0,0,"{}"'.format(scheme, client_id, username, password, path))

    def connect_mqtt_broker(self, host: str, port: int, reconnect: bool = True):
        """
        连接到 MQTT Broker

        Args:
            host: MQTT Broker 地址
            port: 端口
            reconnect: 是否自动重连
        """
        self.iot.register_msg_handler("+MQTTCONNECTED", lambda str: setattr(self, 'mqtt_connected', True))
        self.iot.register_msg_handler("+MQTTDISCONNECTED", lambda str: setattr(self, 'mqtt_connected', False))
        self.iot.register_msg_handler("MQTTSUBRECV", self.handle_mqtt_message)

        retry_count = 3
        while retry_count > 0 and not self.mqtt_connected:
            self.iot.send_at('AT+MQTTCONN=0,"{}",{},{}'.format(host, port, 0 if reconnect else 1))
            time.sleep_ms(3500)
            retry_count -= 1

        # 重新订阅之前注册的 Topic
        for topic, qos in self.mqtt_sub_qos.items():
            self.mqtt_sub_qos[topic] = qos
            self.iot.send_at('AT+MQTTSUB=0,"{}",{}'.format(topic,qos))

    def handle_mqtt_message(self,msg: str):
        """
        处理收到的 MQTT 消息
        """
        try:
            parts = msg.split(",", 4)
            topic = parts[1].strip('"')
            message = parts[3].rstrip('"')
            if topic in self.mqtt_sub_handlers:
                self.mqtt_sub_handlers[topic](message)
        except Exception as e:
            pass

    def is_mqtt_connected(self):
        """
        判断当前是否已连接到 MQTT Broker
        """
        return self.mqtt_connected

    def publish_mqtt_message(self, topic: str, message: str, qos: int = 0):
        """
        发布 MQTT 消息

        Args:
            topic: 主题
            message: 消息内容
            qos: QoS 等级 (0, 1, 2)
        """
        self.iot.send_at('AT+MQTTPUB=0,"{}","{}",{},0'.format(topic,message,qos))

    def on_mqtt_message(self, topic: str, qos: int, handler):
        """
        注册某个 Topic 的回调函数

        Args:
            topic: 主题
            qos: QoS 等级
            handler: 回调函数，接收一个参数：message
        """
        def wrapper(*args):
            if len(args) != 1:
                raise TypeError("handler must accept exactly one argument")
            return handler(*args)
        
        self.mqtt_sub_handlers[topic] = wrapper
        self.mqtt_sub_qos[topic] = qos
        self.iot.send_at('AT+MQTTSUB=0,"{}",{}'.format(topic,qos))

    def disconnect_mqtt_broker(self):
        """
        断开与 MQTT Broker 的连接
        """
        self.iot.remove_msg_handler("MQTTSUBRECV")
        self.iot.remove_msg_handler("+MQTTDISCONNECTED")
        self.iot.remove_msg_handler("+MQTTCONNECTED")
        self.iot.send_at("AT+MQTTCLEAN=0")
        self.mqtt_connected = False

    

#THINKSPEAK模块
class ESP8266_ThingSpeak:
    THINGSPEAK_HOST = "api.thingspeak.com"
    THINGSPEAK_PORT = "80"

    def __init__(self, iot_instance):
        """
        初始化 ThingSpeak 模块
        """
        self.iot = iot_instance
        self.connected = False
        self.data_cmd = ""

    def connect(self):
        """
        模拟连接 ThingSpeak（仅标记状态）
        """
        self.connected = True

    def set_data(self, write_api_key: str,
                 field1=0, field2=0, field3=0, field4=0,
                 field5=0, field6=0, field7=0, field8=0):
        """
        设置要上传的数据

        Args:
            write_api_key: 写入 API Key
            field1~field8: 各个字段的值
        """
        self.data_cmd = 'AT+HTTPCLIENT=2,0,"http://api.thingspeak.com/update?api_key={}&field1={}&field2={}&field3={}&field4={}&field5={}&field6={}&field7={}&field8={}",,,1'.format(
            write_api_key, field1, field2, field3, field4,
            field5, field6, field7, field8
        )

    def upload_data(self):
        """
        上传数据到 ThingSpeak
        """
        if not self.connected:
            raise Exception("Not connected to ThingSpeak")

        self.iot.send_at(self.data_cmd)
        time.sleep_ms(200)

    def is_connected(self):
        """
        返回当前是否连接到 ThingSpeak
        """
        return self.connected
        
#SMARTIOT模块
class ESP8266_SmartIoT:
    class SwitchState:
        ON = 1
        OFF = 2

    def __init__(self, iot_instance):
        """
        初始化 SmartIoT 模块
        """
        self.iot = iot_instance
        self.smartiot_connected = False
        self.smartiot_switch_status = False
        self.smartiot_send_msg = ""
        self.smartiot_last_send_time = 0
        self.smartiot_token = ""
        self.smartiot_topic = ""
        self.smartiot_host = "http://www.smartiot.space"
        self.smartiot_port = "8080"
        self.handlers = {}
        self.polling_started = False

    def connect_smartiot(self, user_token, topic):
        """
        连接到 SmartIoT 平台并获取初始开关状态
        Args:
            user_token (str): 用户 token
            topic (str): 主题名称
        """
        self.smartiot_token = user_token
        self.smartiot_topic = topic

        for _ in range(3):
            url = "/iot/iotTopic/getTopicStatus/{0}/{1}".format(user_token, topic)
            full_url = "{0}:{1}{2}".format(self.smartiot_host, self.smartiot_port, url)
            cmd = 'AT+HTTPCLIENT=2,0,"{0}",,,1'.format(full_url)
            res = self.iot.send_request(cmd, '"code":200', 2000)

            if res:
                self.smartiot_connected = True
                if '"data":"switchOn"' in res:
                    self.smartiot_switch_status = True
                return
            else:
                self.smartiot_connected = False

        self.smartiot_connected = False

    def set_data(self,
                 data1=0, data2=0, data3=0, data4=0,
                 data5=0, data6=0, data7=0, data8=0):
        """
        设置要上传的数据（最多 8 个）

        Args:
            data1~data8: 要上传的数值
        """
        query = (
            "?userToken={0}&topicName={1}"
            "&data1={2}&data2={3}&data3={4}&data4={5}"
            "&data5={6}&data6={7}&data7={8}&data8={9}"
        ).format(
            self.smartiot_token, self.smartiot_topic,
            data1, data2, data3, data4,
            data5, data6, data7, data8
        )

        url = "{0}/iot/iotTopicData/addTopicData{1}".format(
            "{0}:{1}".format(self.smartiot_host, self.smartiot_port), query
        )
        self.smartiot_send_msg = 'AT+HTTPCLIENT=2,0,"{0}",,,1'.format(url)

    def upload_data(self):
        """
        上传设置好的数据到 SmartIoT
        """
        if not self.smartiot_connected or not self.smartiot_send_msg:
            return

        now = time.ticks_ms()
        wait_time = max(0, self.smartiot_last_send_time + 1000 - now)
        if wait_time > 0:
            time.sleep_ms(wait_time)

        self.iot.send_at(self.smartiot_send_msg)
        self.smartiot_last_send_time = now

    def is_connected(self):
        """
        返回当前是否连接 SmartIoT
        """
        return self.smartiot_connected

    def on_switch_event(self, state, handler):
        """
        注册开关事件处理函数

        Args:
            state: SwitchState.ON 或 SwitchState.OFF
            handler: 回调函数
        """
        trigger = '"data":"switchOn"' if state == self.SwitchState.ON else '"data":"switchOff"'
        def wrapped_handler(msg : str):
            if '"data":"switchOn"' in msg and not self.smartiot_switch_status and self.smartiot_connected:
                handler()
                self.smartiot_switch_status = True
            elif '"data":"switchOff"' in msg and self.smartiot_switch_status and self.smartiot_connected:
                handler()
                self.smartiot_switch_status = False
        self.iot.register_msg_handler(trigger, wrapped_handler)

        if not self.polling_started:
            self._start_polling()

    def _start_polling(self):
        if self.polling_started:
            return
    
        def poll_switch_status():
            if self.smartiot_connected:
                url = "/iot/iotTopic/getTopicStatus/{0}/{1}".format(
                    self.smartiot_token, self.smartiot_topic
                )
                full_url = "{0}:{1}{2}".format(
                    self.smartiot_host, self.smartiot_port, url
                )
                cmd = 'AT+HTTPCLIENT=2,0,"{0}",,,1'.format(full_url)
                self.iot.send_at(cmd)
    
        #每秒一次的轮询任务
        run_every(poll_switch_status, s=1)
        self.polling_started = True

#IFTTT模块
class ESP8266_IFTTT:
    def __init__(self, iot_instance):
        self.iot = iot_instance
        self.ifttt_key = ""
        self.ifttt_event = ""

    def set_ifttt(self, key: str, event: str):
        self.ifttt_key = key
        self.ifttt_event = event

    def post_ifttt(self, value1: str = "", value2: str = "", value3: str = ""):
        if not self.ifttt_key or not self.ifttt_event:
            raise ValueError("IFTTT key 或 event 尚未设置，请先调用 set_ifttt()")

        url = "http://maker.ifttt.com/trigger/{}/with/key/{}".format(self.ifttt_event,self.ifttt_key)

        json_data = '{{"value1":"{}","value2":"{}","value3":"{}"}}'.format(
            value1.replace('"', '\\"'),
            value2.replace('"', '\\"'),
            value3.replace('"', '\\"')
        )
        at_cmd = 'AT+HTTPCLIENT=3,1,"{}",,,2,"{}"'.format(url,json_data)
        self.iot.send_at(at_cmd, timeout=1000)


IoT = ESP8266_IoT(ESP8266_IoT.J1)
smartiot = ESP8266_SmartIoT(IoT)
# 注册开关事件
def on_switch_on():
    display.show(Image.HEART_SMALL)

def on_switch_off():
    display.show(Image.HAPPY)

smartiot.on_switch_event(ESP8266_SmartIoT.SwitchState.ON, on_switch_on)
smartiot.on_switch_event(ESP8266_SmartIoT.SwitchState.OFF, on_switch_off)

IoT.connect_wifi("your_wifi_name","your_wifi_password")
while True:
    while True:
        if IoT.wifi_state():
            display.show(Image.HEART)
            sleep(1000)
            if smartiot.is_connected():
                display.show(Image.YES)
                smartiot.set_data(999,888,123)
                smartiot.upload_data()
            else:
                smartiot.connect_smartiot("your_usertoken","1")
            sleep(1000)
        else:
            display.show(Image.NO)
            IoT.connect_wifi("your_wifi_name","your_wifi_password")
        
            