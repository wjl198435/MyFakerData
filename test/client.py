"""
This module contains the main agent client for connecting to the Cayenne server. The client connects
to server, retrives system info as well as sensor and actuator info and sends that data to the server.
It also responds messages from the server, to set actuator values, change system config settings, etc.
"""
import sys
sys.path.append("..")
from json import dumps, loads
from threading import Thread, Event
from time import strftime, localtime, tzset, time, sleep
from queue import Queue, Empty
# from myDevices import __version__
from utils.config import Config, APP_SETTINGS, NETWORK_SETTINGS
from utils.logger import exception, info, warn, error, debug, logJson,setDebug
# from myDevices.sensors import sensors
# from system.hardware import Hardware
from Scheduler.scheduler import SchedulerEngine
# from myDevices.cloud.updater import Updater
# from myDevices.system.systemconfig import SystemConfig
from utils.daemon import Daemon
from utils.threadpool import ThreadPool
# from myDevices.utils.history import History
from utils.subprocess import executeCommand
# from hashlib import sha256
from cloud.apiclient import CayenneApiClient
import cloud.cayennemqtt as cayennemqtt
from config import MQTT_BROKER,MQTT_PORT,MQTT_USER,MQTT_PSW,MQTT_CLIENT_ID
from Tasks.SchedulerManager import SchedulerManager
from DBManager.CrawlPigPrice import get_pig_price

GENERAL_SLEEP_THREAD = 0.20



class ProcessorThread(Thread):
    """Class for processing messages from the server on a thread"""

    def __init__(self, name, client):
        """Initialize processor thread"""
        debug('ProcessorThread init')
        Thread.__init__(self, name=name)
        self.cloudClient = client
        self.Continue = True

    def run(self):
        """Process messages from the server until the thread is stopped"""
        debug('ProcessorThread run,  continue: ' + str(self.Continue))
        while self.Continue:
            try:
                if self.cloudClient.exiting.wait(GENERAL_SLEEP_THREAD):
                    return
                self.cloudClient.ProcessMessage()
            except:
                exception("ProcessorThread Unexpected error")
        return

    def stop(self):
        """Stop processing messages from the server"""
        debug('ProcessorThread stop')
        self.Continue = False

class WriterThread(Thread):
    """Class for sending messages to the server on a thread"""

    def __init__(self, name, client):
        """Initialize writer thread"""
        debug('WriterThread init')
        Thread.__init__(self, name=name)
        self.cloudClient = client
        self.Continue = True

    def run(self):
        """Send messages to the server until the thread is stopped"""
        debug('WriterThread run')
        index = 0
        while self.Continue:

            # debug('WriterThread run')
            # self.cloudClient.mqttClient.publish_packet("topic", "message index:"+str(index))
            # index +=1
            # # print("message index:"+str(index))
            # self.cloudClient.EnqueuePacket("{},index={}".format(self.cloudClient.get_scheduled_events(),str(index)))

            try:
                if self.cloudClient.exiting.wait(GENERAL_SLEEP_THREAD):
                    return
                if self.cloudClient.mqttClient.connected == False:
                    info('WriterThread mqttClient not connected')
                    continue


                got_packet = False
                topic, message = self.cloudClient.DequeuePacket()
                if topic or message:
                    got_packet = True
                try:
                    if message or topic == cayennemqtt.JOBS_TOPIC:
                        # debug('WriterThread, topic: {} {}'.format(topic, message))
                        if not isinstance(message, str):
                            message = dumps(message)
                        self.cloudClient.mqttClient.publish_packet(topic, message)
                        message = None
                except:
                    exception("WriterThread publish packet error")
                finally:
                    if got_packet:
                        self.cloudClient.writeQueue.task_done()
            except:
                exception("WriterThread unexpected error")
        return

    def stop(self):
        """Stop sending messages to the server"""
        debug('WriterThread stop')
        self.Continue = False


class TimerThread(Thread):
    """Class to run a function on a thread at timed intervals"""

    def __init__(self, function, interval, initial_delay=0):
        """Set function to run at intervals and start thread"""
        Thread.__init__(self)
        self.setDaemon(True)
        self.function = function
        self.interval = interval
        self.initial_delay = initial_delay
        self.start()

    def run(self):
        """Run function at intervals"""
        sleep(self.initial_delay)
        while True:
            try:
                self.function()
                sleep(self.interval)
            except:
                exception("TimerThread Unexpected error")


class CloudServerClient:
    """Class to connect to the server and send and receive data"""

    def __init__(self, host, port, cayenneApiHost):
        """Initialize the client configuration"""
        self.HOST = host
        self.PORT = port
        self.CayenneApiHost = cayenneApiHost
        self.config = Config(APP_SETTINGS)
        self.networkConfig = Config(NETWORK_SETTINGS)
        self.username = self.config.get('Agent', 'Username', None)
        self.password = self.config.get('Agent', 'Password', None)
        self.clientId = self.config.get('Agent', 'ClientID', None)
        self.connected = False
        self.exiting = Event()
        self.schedulerEngine = None


    def __del__(self):
        """Delete the client"""
        self.Destroy()




    def Start(self):
        if not self.Connect():
            error('Error starting agent')
            return

        self.readQueue = Queue()
        self.writeQueue = Queue()

        self.writerThread = WriterThread('writer', self)
        self.writerThread.start()

        self.processorThread = ProcessorThread('processor', self)
        self.processorThread.start()

        self.schedulerEngine = SchedulerEngine(self, 'client_scheduler')
        events = self.schedulerEngine.get_scheduled_events()
        self.EnqueuePacket(events, cayennemqtt.JOBS_TOPIC)

        SchedulerManager(self)



    def get_scheduled_events(self):
        self.schedulerEngine = SchedulerEngine(self, 'client_scheduler')
        events = self.schedulerEngine.get_scheduled_events()
        return events

    def OnMessage(self, message):
        """Add message from the server to the queue"""
        info('OnMessage: {}'.format(message))
        self.readQueue.put(message)


    def Connect(self):
        """Connect to the server"""
        self.connected = False
        count = 0
        while self.connected == False and count < 30 and not self.exiting.is_set():
            try:
                self.mqttClient = cayennemqtt.CayenneMQTTClient()
                self.mqttClient.on_message = self.OnMessage
                # info("-----------------------Connect :{} {} {} {} {}".format(self.username,self.password,self.clientId,self.HOST,self.PORT))
                self.mqttClient.begin(self.username, self.password, self.clientId, self.HOST, self.PORT)
                self.mqttClient.loop_start()

                self.connected = True
            except OSError as oserror:
                Daemon.OnFailure('cloud', oserror.errno)
                error('Connect failed: ' + str(self.HOST) + ':' + str(self.PORT) + ' Error:' + str(oserror))
                if self.exiting.wait(30):
                    # If we are exiting return immediately
                    return self.connected
                count += 1
        return self.connected

    def DequeuePacket(self):
        """Dequeue a message packet to send to the server"""
        packet = (None, None)
        try:
            packet = self.writeQueue.get(False)
        except Empty:
            pass
        return packet

    def EnqueuePacket(self, message, topic=cayennemqtt.DATA_TOPIC):
        """Enqueue a message packet to send to the server"""
        packet = (topic, message)
        self.writeQueue.put(packet)

    def Disconnect(self):
        """Disconnect from the server"""
        Daemon.Reset('cloud')
        try:
            if hasattr(self, 'mqttClient'):
                self.mqttClient.loop_stop()
                info('myDevices cloud disconnected')
        except:
            exception('Error stopping client')

    def Destroy(self):
        """Destroy client and stop client threads"""
        info('Shutting down client')
        self.exiting.set()
        if hasattr(self, 'sensorsClient'):
            pass
            # self.sensorsClient.StopMonitoring()
        if hasattr(self, 'schedulerEngine'):
            self.schedulerEngine.stop()
        if hasattr(self, 'updater'):
            self.updater.stop()
        if hasattr(self, 'writerThread'):
            self.writerThread.stop()
        if hasattr(self, 'processorThread'):
            self.processorThread.stop()
        ThreadPool.Shutdown()
        self.Disconnect()
        info('Client shut down')

    def RunAction(self, action):
        info('RunAction:' + action)
        eval(action)()
        # action()
        # partial(action)
        # job()
        # self.actions_ran.append(action)
        # info(self.actions_ran)
        return True

    # def RunAction(self, action):
    #     """Run a specified action"""
    #     debug('RunAction: {}'.format(action))
    #     # result = True
    #     # command = action.copy()
    #     # self.mqttClient.transform_command(command)
    #     # result = self.ExecuteMessage(command)
    #     # return result

    def ProcessMessage(self):
        """Process a message from the server"""
        try:
            messageObject = self.readQueue.get(False)
            if not messageObject:
                return False
        except Empty:
            return False

        info(messageObject)
        # self.ExecuteMessage(messageObject)


def on_message_test(client, obj, msg):

    print ("MESSAGE: "+msg.topic+" "+str(msg.qos)+" "+str(msg.payload))

if __name__ == '__main__':
    setDebug()
    client = CloudServerClient(MQTT_BROKER,MQTT_PORT,"192.168.8.102")
    client.Start()

    while client.mqttClient.connected is False:
        pass

    if client.mqttClient.connected == True:
        info("MQTT Client connect is success!------------")
        # client.mqttClient.client.subscribe("test", True)
        topic = "test2019"
        client.mqttClient.client.subscribe("test", True)
        client.mqttClient.client.subscribe(topic,True)
        # client.mqttClient.client.publish(topic='test', payload='hello world!! ' , qos=1, retain=False )
        client.mqttClient.client.message_callback_add(topic, on_message_test )

        config_topic = "binary_sensor/jack11/jack11/config"
        message = {"name": "garden88", "device_class": "motion", "state_topic": "homeassistant/binary_sensor/garden/state"}
        client.EnqueuePacket( message, topic=config_topic)

    # "homeassistant/binary_sensor/garden/config" -m '{"name": "garden10", "device_class": "motion", "state_topic": "homeassistant/binary_sensor/garden/state"}'