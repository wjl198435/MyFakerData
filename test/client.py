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

GENERAL_SLEEP_THREAD = 0.20




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
            index +=1
            # print("message index:"+str(index))
            self.cloudClient.EnqueuePacket("{},index={}".format(self.cloudClient.get_scheduled_events(),str(index)))

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

        self.schedulerEngine = SchedulerEngine(self, 'client_scheduler')
        events = self.schedulerEngine.get_scheduled_events()
        self.EnqueuePacket(events, cayennemqtt.JOBS_TOPIC)
    def get_scheduled_events(self):
        self.schedulerEngine = SchedulerEngine(self, 'client_scheduler')
        events = self.schedulerEngine.get_scheduled_events()
        return events

    def OnMessage(self, message):
        pass
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

if __name__ == '__main__':
    setDebug()
    client = CloudServerClient("192.168.8.102",1883,"192.168.8.102")
    client.Start()