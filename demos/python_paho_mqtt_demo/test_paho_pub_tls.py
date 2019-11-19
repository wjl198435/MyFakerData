#!/usr/bin/env python

############################################################################
# Date: 2017-11-15
############################################################################
# Author: Rawat S. 
#   (Dept. of Electrical & Computer Engineering, KMUTNB, Bangkok/Thailand)
#
############################################################################
# Short Description:
#   This Python script uses the paho-mqtt package to publish a message to
#   an MQTT broker listening on the port number 8883 (secure).
#   This script has been tested with Ubuntu Linux (16.04 LTS).
#
############################################################################

import paho.mqtt.publish as publish
import paho.mqtt.client as mqtt
import ssl
import sys, time

mqtt_hostname = "localhost"  # specify the hostname of the target MQTT broker
mqtt_port = 8883

mqtt_auth = {
  'username':'XXXXXXXXXXX',
  'password':'XXXXXXXXXXX'
}

mqtt_tls = {
  'ca_certs':"/etc/ssl/certs/ca-certificates.crt",
  'tls_version':ssl.PROTOCOL_TLSv1_2   # use the TLS v1.2
}

publish.single(
  topic="test",
  payload="hello world !!!",
  hostname=mqtt_hostname,
  client_id="paho-mqtt-test",
  auth=mqtt_auth,
  tls=mqtt_tls,
  port=mqtt_port,
  protocol=mqtt.MQTTv311 )

time.sleep( 1.0 )
print ('Done....')

############################################################################
