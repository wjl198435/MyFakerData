#!/usr/bin/env python

############################################################################
# Date: 2017-11-15
############################################################################
# Author: Rawat S. 
#   (Dept. of Electrical & Computer Engineering, KMUTNB, Bangkok/Thailand)
#
############################################################################
# Short Description:
#   This Python script uses the paho-mqtt package to connect to 
#   an MQTT broker in order to publish and subscribe messages 
#   on a specific topic.
#   The MQTT broker listens on the port number 8883 (secure).
#   This script has been tested with Ubuntu Linux (16.04 LTS).
#
############################################################################

import paho.mqtt.client as mqtt
import sys, time

mqtt_hostname = "localhost"
mqtt_port = 8883

auth_user = '<username>'
auth_pass = '<password>'

count=1
run=True

def on_message_test(client, obj, msg):
    global count, run
    print ("MESSAGE: "+msg.topic+" "+str(msg.qos)+" "+str(msg.payload))
    count = count+1
    if count < 10:
        client.publish(topic='test', payload='hello world!! %d' % count, qos=1, retain=False )
    else:
        run = False

def on_message(client, obj, msg):
    print (msg.topic+" "+str(msg.qos)+" "+str(msg.payload))

def on_publish(client, userdata, mid):
    print ("message published", str(mid) )

def on_subscribe(client, obj, mid, qos):
    print ("client subscribed")

def on_connect(client, userdata, flags, rc):
    global count
    print ("client connected")
    client.subscribe("test", qos=1)
    client.publish(topic='test', payload='hello world!! %d' % count , qos=1, retain=False )

client = mqtt.Client('paho-mqtt-test')

client.message_callback_add( "test", on_message_test )

client.on_message   = on_message
client.on_publish   = on_publish
client.on_subscribe = on_subscribe
client.on_connect   = on_connect

client.username_pw_set( auth_user, auth_pass )
client.tls_set( '/etc/ssl/certs/ca-certificates.crt', tls_version=2 ) # TLSv1.2
client.connect( mqtt_hostname, mqtt_port, 60 )

try:
    while run:
        client.loop()
        time.sleep(0.5)

except KeyboardInterrupt:
    print ( 'Terminated....' )

print ( 'Done' )

##########################################################################
