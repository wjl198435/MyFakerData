# from config import DB_URL
# print(DB_URL)
from cloud.client import CloudServerClient
from utils.logger import exception, setDebug, info, debug, error, logToFile, setInfo
import cloud.cayennemqtt as cayennemqtt
from time import sleep
import warnings
import paho.mqtt.client as mqtt

# class CloudServerClient:
#     """Class to connect to the server and send and receive data"""
#     def OnMessage(self, message):
#         self.receivedMessage = message
#         # print('OnMessage: {}'.format(self.receivedMessage))
#
#
#
#     def __init__(self, host, port, cayenneApiHost):
#         """Initialize the client configuration"""
#         self.HOST = host
#         self.PORT = port
#         self.CayenneApiHost = cayenneApiHost
#
#         self.mqttClient = cayennemqtt.CayenneMQTTClient()
#         self.mqttClient.on_message = self.OnMessage
#         self.mqttClient.begin("demo", "demo", "demo_wd", "192.168.8.102", 1883)
#         self.mqttClient.loop_start()
#
#         # self.Start()
#
#     def testPublish(self):
#         #Ignore warning caused by paho mqtt not closing some sockets in the destructor
#         with warnings.catch_warnings():
#             warnings.simplefilter('ignore', ResourceWarning)
#             sentTopic = self.mqttClient.get_topic_string(cayennemqtt.DATA_TOPIC)
#             print(sentTopic)
#             sentMessage = '{"publish_test":"data"}'
#             self.mqttClient.publish_packet(cayennemqtt.DATA_TOPIC, sentMessage,1)
#             # sleep(1)
#         # self.config = Config(APP_SETTINGS)
#         # self.networkConfig = Config(NETWORK_SETTINGS)
#         # self.username = self.config.get('Agent', 'Username', None)
#         # self.password = self.config.get('Agent', 'Password', None)
#         # self.clientId = self.config.get('Agent', 'ClientID', None)
#         # self.connected = False
#         # self.exiting = Event()
#
#     def Start(self):
#         self.mqttClient = cayennemqtt.CayenneMQTTClient()
#         self.mqttClient.on_message = self.OnMessage
#         self.mqttClient.begin("demo", "demo", "demo_wd", "192.168.8.102", 1883)
#         self.mqttClient.loop_start()
#         sleep(10)


mqttClient = mqtt.Client()


def disconnect_callback(self, client, userdata, rc):
    """The callback for when the client disconnects from the server.
    client is the client instance for this callback.
    userdata is the private user data as set in Client() or userdata_set().
    rc is the connection result.
    """
    # info("disconnect_callback->Disconnected with result code "+str(client)+":"+str(userdata))
    info("Disconnected with result code "+str(rc))
    self.connected = False
    reconnected = False
    while not reconnected:
        try:
            self.client.reconnect()
            reconnected = True
        except:
            print("Reconnect failed, retrying")
            time.sleep(5)

mqttClient.on_disconnect = disconnect_callback
#连接MQTT服务器


def on_mqtt_connect():
    mqttClient.connect("192.168.8.102", 1883, 60)
    mqttClient.loop_start()
# publish 消息
def on_publish(topic, payload, qos):
    print("on_publish")
    mqttClient.publish(topic, payload, qos)
# 消息处理函数
def on_message_come(lient, userdata, msg):
    print(msg.topic + " " + ":" + str(msg.payload))
    # subscribe 消息
def on_subscribe():
    print("on_publish")
    mqttClient.subscribe("/server", 1)
    mqttClient.on_message = on_message_come # 消息到来处理函数



if __name__ == "__main__":
    # on_publish("v1/demo/things/demo_wd/data/json", "Hello Python!", 1)
    setDebug()
    client = CloudServerClient("192.168.8.102", 1883, "192.168.8.102")
    client.Start()
    for i in range(10):
        print(i)
        client.SendSystemInfo()
        sleep(1)

    # # client.Start()


    # on_mqtt_connect()
    # for i in range(10):
    #     on_publish("v1/demo/things/demo_wd/data/json", "Hello Python!", 1)
    #     sleep(1)


