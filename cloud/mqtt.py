import sys
sys.path.append("..")
from cloud.client import CloudServerClient
from utils.logger import exception, setDebug, info, debug, error, logToFile, setInfo
import cloud.cayennemqtt as cayennemqtt
from time import sleep
import warnings
import paho.mqtt.client as mqtt

COMMAND_TOPIC = 'cmd'
COMMAND_JSON_TOPIC = 'cmd.json'

class CloudServerClient:
    """Class to connect to the server and send and receive data"""
    def OnMessage(self, message):
        self.receivedMessage = message
        print('OnMessage: {}'.format(self.receivedMessage))



    def __init__(self, host, port, cayenneApiHost):
        """Initialize the client configuration"""
        self.HOST = host
        self.PORT = port
        self.CayenneApiHost = cayenneApiHost
        self.username = "demo"
        self.clientid = "demo_wd"
        self.passwd =  "demo"

        self.root_topic = 'v1/{}/things/{}'.format(self.username, self.clientid)
        self.mqttClient = cayennemqtt.CayenneMQTTClient()
        self.mqttClient.on_message = self.OnMessage
        self.mqttClient.begin(self.username,self.passwd , self.clientid, self.HOST, self.PORT)
        self.mqttClient.loop_start()

        print(self.get_topic_string(COMMAND_TOPIC,True))

        # self.mqttClient.client.subscribe(self.get_topic_string(COMMAND_TOPIC, True))
        # self.mqttClient.client.subscribe(self.get_topic_string(COMMAND_JSON_TOPIC, False))

        # self.Start()

    def get_topic_string(self, topic, append_wildcard=False):
        """Return a topic string.

        topic: the topic substring
        append_wildcard: if True append the single level topics wildcard (+)"""
        if append_wildcard:
            return '{}/{}/+'.format(self.root_topic, topic)
        else:
            return '{}/{}'.format(self.root_topic, topic)

    def testPublish(self):
        #Ignore warning caused by paho mqtt not closing some sockets in the destructor
        with warnings.catch_warnings():
            warnings.simplefilter('ignore', ResourceWarning)
            sentTopic = self.mqttClient.get_topic_string(cayennemqtt.DATA_TOPIC)
            print(sentTopic)
            sentMessage = '{"publish_test":"data"}'
            self.mqttClient.publish_packet(cayennemqtt.DATA_TOPIC, sentMessage,1)
    def mqtt_publish(self,topic,message):
        #Ignore warning caused by paho mqtt not closing some sockets in the destructor
        with warnings.catch_warnings():
            warnings.simplefilter('ignore', ResourceWarning)
            # sentTopic = self.mqttClient.get_topic_string(cayennemqtt.DATA_TOPIC)
            # print(sentTopic)

            self.mqttClient.publish_packet(topic, message,1)



if __name__ == "__main__":
    setDebug()
    client = CloudServerClient("192.168.8.102", 1883, "192.168.8.102")

    for i in range(10):
        print(i)
        client.mqtt_publish("test1","2")
        sleep(1)