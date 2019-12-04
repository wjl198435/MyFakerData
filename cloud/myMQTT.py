import paho.mqtt.client as mqtt

def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))

def on_message(client, userdata, msg):
    print(msg.topic+" "+str(msg.payload))

client = mqtt.Client()
print("???")
client.on_connect = on_connect
client.on_message = on_message
client.connect("192.168.8.102", 1883, 600)
client.publish('emqtt',payload='Hello,EMQ!',qos=0)
client.loop_start()