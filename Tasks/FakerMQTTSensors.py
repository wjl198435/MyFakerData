import paho.mqtt.client as mqtt
import sys
sys.path.append("..")
from config import MQTTHOST, MQTTPORT


mqttClient = mqtt.Client()
# 连接MQTT服务器
def on_mqtt_connect():
    mqttClient.connect(MQTTHOST, MQTTPORT, 60)
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