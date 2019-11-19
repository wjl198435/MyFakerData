import sys
sys.path.append("..")
from cloud.client import CloudServerClient
from utils.logger import exception, setDebug, info, debug, error, logToFile, setInfo
import cloud.cayennemqtt as cayennemqtt
from time import sleep
import warnings
import paho.mqtt.client as mqtt
class CloudServerClient:
    """Class to connect to the server and send and receive data"""
    def OnMessage(self, message):
        self.receivedMessage = message
        # print('OnMessage: {}'.format(self.receivedMessage))



    def __init__(self, host, port, cayenneApiHost):
        """Initialize the client configuration"""
        self.HOST = host
        self.PORT = port
        self.CayenneApiHost = cayenneApiHost

        self.mqttClient = cayennemqtt.CayenneMQTTClient()
        self.mqttClient.on_message = self.OnMessage
        self.mqttClient.begin("demo", "demo", "demo_wd", "192.168.8.102", 1883)
        self.mqttClient.loop_start()

        # self.Start()

    def testPublish(self):
        #Ignore warning caused by paho mqtt not closing some sockets in the destructor
        with warnings.catch_warnings():
            warnings.simplefilter('ignore', ResourceWarning)
            sentTopic = self.mqttClient.get_topic_string(cayennemqtt.DATA_TOPIC)
            print(sentTopic)
            sentMessage = '{"publish_test":"data"}'
            self.mqttClient.publish_packet(cayennemqtt.DATA_TOPIC, sentMessage,1)
            # sleep(1)
        # self.config = Config(APP_SETTINGS)
        # self.networkConfig = Config(NETWORK_SETTINGS)
        # self.username = self.config.get('Agent', 'Username', None)
        # self.password = self.config.get('Agent', 'Password', None)
        # self.clientId = self.config.get('Agent', 'ClientID', None)
        # self.connected = False
        # self.exiting = Event()

if __name__ == "__main__":
    setDebug()
    client = CloudServerClient("192.168.8.102", 1883, "192.168.8.102")

    for i in range(10):
        print(i)
        client.testPublish()
        sleep(1)