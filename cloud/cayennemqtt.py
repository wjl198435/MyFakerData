import time
from json import loads, decoder
from ssl import PROTOCOL_TLSv1_2
import paho.mqtt.client as mqtt
from utils.logger import debug, error, exception, info, logJson, warn

# Topics
DATA_TOPIC = 'data/json'
COMMAND_TOPIC = 'cmd'
COMMAND_JSON_TOPIC = 'cmd.json'
COMMAND_RESPONSE_TOPIC = 'response'
JOBS_TOPIC = 'jobs.json'



# Data Channels
SYS_POWER = "sys:power"
SYS_HARDWARE_MAKE = 'sys:hw:make'
SYS_HARDWARE_MODEL = 'sys:hw:model'
SYS_OS_NAME = 'sys:os:name'
SYS_OS_VERSION = 'sys:os:version'
SYS_NET = 'sys:net'
SYS_STORAGE = 'sys:storage'
SYS_RAM = 'sys:ram'
SYS_CPU = 'sys:cpu'
SYS_I2C = 'sys:i2c'
SYS_SPI = 'sys:spi'
SYS_UART = 'sys:uart'
SYS_ONEWIRE = 'sys:1wire'
SYS_DEVICETREE = 'sys:devicetree'
SYS_GPIO = 'sys:gpio'
SYS_POWER_RESET = 'sys:pwr:reset'
SYS_POWER_HALT = 'sys:pwr:halt'
AGENT_VERSION = 'agent:version'
AGENT_DEVICES = 'agent:devices'
AGENT_MANAGE = 'agent:manage'
AGENT_SCHEDULER = 'agent:scheduler'
DEV_SENSOR = 'dev'

# Channel Suffixes
IP = 'ip'
SPEEDTEST = 'speedtest'
SSID = 'ssid'
USAGE = 'usage'
CAPACITY = 'capacity'
LOAD = 'load'
TEMPERATURE = 'temp'
VALUE = 'value'
FUNCTION = 'function'


class DataChannel:
    @staticmethod
    def add(data_list, prefix, channel=None, suffix=None, value=None, type=None, unit=None, name=None):
        """Create data channel dict and append it to a list"""
        data_channel = prefix
        if channel is not None:
            data_channel += ':' + str(channel)
        if suffix is not None:
            data_channel += ';' + str(suffix)
        data = {}
        data['channel'] = data_channel
        data['value'] = value
        if type is not None:
            data['type'] = type
        if unit is not None:
            data['unit'] = unit
        if name is not None:
            data['name'] = name
        data_list.append(data)

    @staticmethod
    def add_unique(data_list, prefix, channel=None, suffix=None, value=None, type=None, unit=None, name=None):
        """Create data channel dict and append it to a list if the channel doesn't already exist in the list"""
        data_channel = prefix
        if channel is not None:
            data_channel += ':' + str(channel)
        if suffix is not None:
            data_channel += ';' + str(suffix)
        item = next((item for item in data_list if item['channel'] == data_channel), None)
        if not item:
            data = {}
            data['channel'] = data_channel
            data['value'] = value
            if type is not None:
                data['type'] = type
            if unit is not None:
                data['unit'] = unit
            if name is not None:
                data['name'] = name
            data_list.append(data)


class CayenneMQTTClient:
    """Cayenne MQTT Client class.

    This is the main client class for connecting to Cayenne and sending and receiving data.

    Standard usage:
    * Set on_message callback, if you are receiving data.
    * Connect to Cayenne using the begin() function.
    * Call loop() at intervals (or loop_forever() once) to perform message processing.
    * Send data to Cayenne using write functions: virtualWrite(), celsiusWrite(), etc.
    * Receive and process data from Cayenne in the on_message callback.
    The on_message callback can be used by creating a function and assigning it to CayenneMQTTClient.on_message member.
    The callback function should have the following signature: on_message(topic, message)
    If it exists this callback is used as the default message handler.
    """
    client = None
    root_topic = ""
    connected = False
    on_message = None

    def begin(self, username, password, clientid, hostname='mqtt.mydevices.com', port=8883):
        """Initializes the client and connects to Cayenne.

        username is the Cayenne username.
        password is the Cayenne password.
        clientid is the Cayennne client ID for the device.
        hostname is the MQTT broker hostname.
        port is the MQTT broker port.
        """
        self.root_topic = 'v1/{}/things/{}'.format(username, clientid)
        self.client = mqtt.Client(client_id=clientid, clean_session=True, userdata=self)
        self.client.on_connect = self.connect_callback
        self.client.on_disconnect = self.disconnect_callback
        self.client.on_message = self.message_callback
        self.client.username_pw_set(username, password)
        if port != 1883:
            self.client.tls_set(ca_certs='/etc/ssl/certs/ca-certificates.crt', tls_version=PROTOCOL_TLSv1_2)
        info("self.client.connect hostname = {} ,port ={}".format(hostname,port))
        self.client.connect(hostname, port, 60)
        info('Connecting to {}:{}'.format(hostname, port))



    def connect_callback(self, client, userdata, flags, rc):
        """The callback for when the client connects to the server.
        client is the client instance for this callback.
        userdata is the private user data as set in Client() or userdata_set().
        flags are the response flags sent by the broker.
        rc is the connection result.
        """
        if rc != 0:
            # MQTT broker error codes
            broker_errors = {
                1 : 'unacceptable protocol version',
                2 : 'identifier rejected',
                3 : 'server unavailable',
                4 : 'bad user name or password',
                5 : 'not authorized',
            }
            raise Exception("Connection failed, " + broker_errors.get(rc, "result code " + str(rc)))
        else:
            info("Connected with result code "+str(rc))
            self.connected = True
            # Subscribing in on_connect() means that if we lose the connection and
            # reconnect then subscriptions will be renewed.
            client.subscribe(self.get_topic_string(COMMAND_TOPIC, True))
            client.subscribe(self.get_topic_string(COMMAND_JSON_TOPIC, False))

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

    def transform_command(self, command, payload=[], channel=[]):
        """Transform a command message into an object.
        command is the command object that will be transformed in place.
        payload is an optional list of payload data items.
        channel is an optional list containing channel and suffix data.
        """
        if not payload:
            command['payload'] = command.pop('value')
            channel = command['channel'].split('/')[-1].split(';')
        else:
            if len(payload) > 1:
                command['cmdId'] = payload[0]
                command['payload'] = payload[1]
            else:
                command['payload'] = payload[0]
        command['channel'] = channel[0]
        if len(channel) > 1:
            command['suffix'] = channel[1]

    def message_callback(self, client, userdata, msg):
        """The callback for when a message is received from the server.
        client is the client instance for this callback.
        userdata is the private user data as set in Client() or userdata_set().
        msg is the received message.
        """
        try:
            message = {}
            if msg.topic[-len(COMMAND_JSON_TOPIC):] == COMMAND_JSON_TOPIC:
                message = loads(msg.payload.decode())
                self.transform_command(message)
            else:
                self.transform_command(message, msg.payload.decode().split(','), msg.topic.split('/')[-1].split(';'))
            debug('message_callback: {}'.format(message))
            if self.on_message:
                self.on_message(message)
        except:
            exception('Error processing message: {} {}'.format(msg.topic, str(msg.payload)))

    def get_topic_string(self, topic, append_wildcard=False):
        """Return a topic string.

        topic: the topic substring
        append_wildcard: if True append the single level topics wildcard (+)"""
        if append_wildcard:
            return '{}/{}/+'.format(self.root_topic, topic)
        else:
            return '{}/{}'.format(self.root_topic, topic)

    def disconnect(self):
        """Disconnect from Cayenne.
        """
        self.client.disconnect()

    def loop(self, timeout=1.0):
        """Process Cayenne messages.

        This should be called regularly to ensure Cayenne messages are sent and received.

        timeout: The time in seconds to wait for incoming/outgoing network
          traffic before timing out and returning.
        """
        self.client.loop(timeout)

    def loop_start(self):
        """This is part of the threaded client interface. Call this once to
        start a new thread to process network traffic. This provides an
        alternative to repeatedly calling loop() yourself.
        """
        self.client.loop_start()

    def loop_stop(self):
        """This is part of the threaded client interface. Call this once to
        stop the network thread previously created with loop_start(). This call
        will block until the network thread finishes.
        """
        self.client.loop_stop()

    def publish_packet(self, topic, packet, qos=0, retain=False):
        """Publish a packet.

        topic: topic substring.
        packet: JSON packet to publish.
        qos: quality of service level to use.
        retain: if True, the message will be set as the "last known good"/retained message for the topic.
        """
        debug('Publish to {}'.format(self.get_topic_string(topic)))
        self.client.publish(self.get_topic_string(topic), packet, qos, retain)

    def publish_response(self, msg_id, error_message=None):
        """Send a command response to Cayenne.

        This should be sent when a command message has been received.
        msg_id is the ID of the message received.
        error_message is the error message to send. This should be set to None if there is no error.
        """
        topic = self.get_topic_string(COMMAND_RESPONSE_TOPIC)
        if error_message:
            payload = "error,%s=%s" % (msg_id, error_message)
        else:
            payload = "ok,%s" % (msg_id)
        self.client.publish(topic, payload)