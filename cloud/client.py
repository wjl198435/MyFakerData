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


def GetTime():
    """Return string with the current time"""
    tzset()
    cur = time()
    val = strftime("%Y-%m-%dT%T", localtime(cur))
    timezone = strftime("%z", localtime(cur))
    hourtime = int(timezone[1:3])
    timezone = timezone[:1] + str(int(timezone[1:3]))+':'+ timezone[3:7]
    if hourtime == 0:
        timezone = ''
    return val + timezone


class OSInfo():
    """Class for getting information about the OS"""

    def __init__(self):
        """Initialize variables with OS information"""
        try:
            with open('/etc/os-release', 'r') as os_file:
                for line in os_file:
                    splitLine = line.split('=')
                    if len(splitLine) < 2:
                        continue
                    key = splitLine[0].strip()
                    value = splitLine[1].strip().replace('"', '')
                    keys = ('VERSION_ID', 'ID')
                    if key in keys:
                        setattr(self, key, value)
        except:
            exception("OSInfo Unexpected error")


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
        while self.Continue:
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


    def __del__(self):
        """Delete the client"""
        self.Destroy()

    def Start(self):
        """Connect to server and start background threads"""
        try:
            self.installDate=None
            try:
                self.installDate = self.config.get('Agent', 'InstallDate', fallback=None)
            except:
                pass
            if not self.installDate:
                self.installDate = int(time())
                self.config.set('Agent', 'InstallDate', self.installDate)
            if not self.username and not self.password and not self.clientId:
                self.CheckSubscription()
            if not self.Connect():
                error('Error starting agent')
                return



            self.schedulerEngine = SchedulerEngine(self, 'client_scheduler')
           
            # self.sensorsClient = sensors.SensorsClient()
            self.readQueue = Queue()
            self.writeQueue = Queue()
            # self.hardware = Hardware()
            # self.oSInfo = OSInfo()
            self.count = 10000
            self.buff = bytearray(self.count)
            # self.sensorsClient.SetDataChanged(self.OnDataChanged)
            self.writerThread = WriterThread('writer', self)
            self.writerThread.start()
            self.processorThread = ProcessorThread('processor', self)
            self.processorThread.start()
            self.systemInfo = []

            TimerThread(self.SendSystemInfo, 300)
            # TimerThread(self.SendSystemState, 30, 5)
            # self.updater = Updater(self.config)
            # self.updater.start()
            events = self.schedulerEngine.get_scheduled_events()
            self.EnqueuePacket(events, cayennemqtt.JOBS_TOPIC)
            # self.sentHistoryData = {}
            # self.historySendFails = 0
            # self.historyThread = Thread(target=self.SendHistoryData)
            # self.historyThread.setDaemon(True)
            # self.historyThread.start()



        except Exception as e:
            exception('Initialize error: ' + str(e))

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

    def OnDataChanged(self, data):
        """Enqueue a packet containing changed system data to send to the server"""
        try:
            if len(data) > 15:
                items = [{item['channel']:item['value']} for item in data if not item['channel'].startswith(cayennemqtt.SYS_GPIO)]
                info('Send changed data: {} + {}'.format(items, cayennemqtt.SYS_GPIO))
            else:
                info('Send changed data: {}'.format([{item['channel']:item['value']} for item in data]))
            # items = {}
            # gpio_items = {}
            # for item in data:
            #     if not item['channel'].startswith(cayennemqtt.SYS_GPIO):
            #         items[item['channel']] = item['value']
            #     else:
            #         channel = item['channel'].replace(cayennemqtt.SYS_GPIO + ':', '').split(';')
            #         if not channel[0] in gpio_items:
            #             gpio_items[channel[0]] = str(item['value'])
            #         else:
            #             gpio_items[channel[0]] += ',' + str(item['value'])
            # info('Send changed data: {}, {}: {}'.format(items, cayennemqtt.SYS_GPIO, gpio_items))
        except:
            info('Send changed data')
            pass
        self.EnqueuePacket(data)

    def SendSystemInfo(self):
        """Enqueue a packet containing system info to send to the server"""
        info("SendSystemInfo")
        try:
            currentSystemInfo = []
            cayennemqtt.DataChannel.add(currentSystemInfo, cayennemqtt.SYS_OS_NAME, value="self.oSInfo.ID")
            cayennemqtt.DataChannel.add(currentSystemInfo, cayennemqtt.SYS_OS_VERSION, value="self.oSInfo.VERSION_ID")
            cayennemqtt.DataChannel.add(currentSystemInfo, cayennemqtt.AGENT_VERSION, value="self.config.get('Agent', 'Version', __version__)")
            cayennemqtt.DataChannel.add(currentSystemInfo, cayennemqtt.SYS_POWER_RESET, value=0)
            cayennemqtt.DataChannel.add(currentSystemInfo, cayennemqtt.SYS_POWER_HALT, value=0)
            # config = SystemConfig.getConfig()
            # if config:
            #     channel_map = {'I2C': cayennemqtt.SYS_I2C, 'SPI': cayennemqtt.SYS_SPI, 'Serial': cayennemqtt.SYS_UART,
            #                    'OneWire': cayennemqtt.SYS_ONEWIRE, 'DeviceTree': cayennemqtt.SYS_DEVICETREE}
            #     for key, channel in channel_map.items():
            #         try:
            #             cayennemqtt.DataChannel.add(currentSystemInfo, channel, value=config[key])
            #         except:
            #             pass
            if currentSystemInfo != self.systemInfo:
                data = currentSystemInfo
                if self.systemInfo:
                    data = [x for x in data if x not in self.systemInfo]
                if data:
                    self.systemInfo = currentSystemInfo
                    info('Send system info: {}'.format([{item['channel']:item['value']} for item in data]))
                    self.EnqueuePacket(data)
        except Exception:
            exception('SendSystemInfo unexpected error')

    def CheckSubscription(self):
        """Check that an invite code is valid"""
        inviteCode = self.config.get('Agent', 'InviteCode', fallback=None)
        if not inviteCode:
            error('No invite code found in {}'.format(self.config.path))
            print('Please input an invite code. This can be retrieved from the Cayenne dashboard by adding a new Raspberry Pi device.\n'
                  'The invite code will be part of the script name shown there: rpi_[invitecode].sh.')
            inviteCode = input('Invite code: ')
            if inviteCode:
                self.config.set('Agent', 'InviteCode', inviteCode)
            else:
                print('No invite code set, exiting.')
                raise SystemExit
        inviteCode = self.config.get('Agent', 'InviteCode')
        cayenneApiClient = CayenneApiClient(self.CayenneApiHost)
        credentials = cayenneApiClient.loginDevice(inviteCode)

        # 模拟正常登陆 由于api 接口尚未开发
        credentials={"mqtt":{"username":"demo","password":"demo","clientId":"demo_wd"}}
        if credentials == None:
            error('Registration failed for invite code {}, closing the process'.format(inviteCode))
            raise SystemExit
        else:
            info('Registration succeeded for invite code {}, credentials = {}'.format(inviteCode, credentials))
            self.config.set('Agent', 'Initialized', 'true')
            try:
                self.username = credentials['mqtt']['username']
                self.password = credentials['mqtt']['password']
                self.clientId = credentials['mqtt']['clientId']
                self.config.set('Agent', 'Username', self.username)
                self.config.set('Agent', 'Password', self.password)
                self.config.set('Agent', 'ClientID', self.clientId)
            except:
                exception('Invalid credentials, closing the process')
                raise SystemExit

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

    def Disconnect(self):
        """Disconnect from the server"""
        Daemon.Reset('cloud')
        try:
            if hasattr(self, 'mqttClient'):
                self.mqttClient.loop_stop()
                info('myDevices cloud disconnected')
        except:
            exception('Error stopping client')

    def Restart(self):
        """Restart the server connection"""
        if not self.exiting.is_set():
            debug('Restarting cycle...')
            sleep(1)
            self.Disconnect()
            self.Connect()

    def CheckJson(self, message):
        """Check if a JSON message is valid"""
        try:
            test = loads(message)
        except ValueError:
            return False
        return True

    def OnMessage(self, message):
        """Add message from the server to the queue"""
        info('OnMessage: {}'.format(message))
        self.readQueue.put(message)

    def RunAction(self, action):
        """Run a specified action"""
        debug('RunAction: {}'.format(action))
        result = True
        command = action.copy()
        self.mqttClient.transform_command(command)
        result = self.ExecuteMessage(command)
        return result

    def ProcessMessage(self):
        """Process a message from the server"""
        try:
            messageObject = self.readQueue.get(False)
            if not messageObject:
                return False
        except Empty:
            return False
        self.ExecuteMessage(messageObject)

    def ExecuteMessage(self, message):
        """Execute an action described in a message object

        Returns: True if action was executed, False otherwise."""
        result = False
        if not message:
            return result
        channel = message['channel']
        info('ExecuteMessage: {}'.format(message))
        if channel in (cayennemqtt.SYS_POWER_RESET, cayennemqtt.SYS_POWER_HALT):
            result = self.ProcessPowerCommand(message)
        elif channel.startswith(cayennemqtt.DEV_SENSOR):
            result = self.ProcessSensorCommand(message)
        elif channel.startswith(cayennemqtt.SYS_GPIO):
            result = self.ProcessGpioCommand(message)
        elif channel == cayennemqtt.AGENT_DEVICES:
            result = self.ProcessDeviceCommand(message)
        elif channel in (cayennemqtt.SYS_I2C, cayennemqtt.SYS_SPI, cayennemqtt.SYS_UART, cayennemqtt.SYS_ONEWIRE):
            result = self.ProcessConfigCommand(message)
        elif channel == cayennemqtt.AGENT_MANAGE:
            result = self.ProcessAgentCommand(message)
        elif channel == cayennemqtt.AGENT_SCHEDULER:
            result = self.ProcessSchedulerCommand(message)
        else:
            info('Unknown message')
        return result

    def ProcessPowerCommand(self, message):
        """Process command to reboot/shutdown the system

        Returns: True if command was processed, False otherwise."""
        error_message = None
        try:
            self.EnqueueCommandResponse(message, error_message)
            commands = {cayennemqtt.SYS_POWER_RESET: 'sudo shutdown -r now', cayennemqtt.SYS_POWER_HALT: 'sudo shutdown -h now'}
            if int(message['payload']) == 1:
                debug('Processing power command')
                data = []
                cayennemqtt.DataChannel.add(data, message['channel'], value=1)
                self.EnqueuePacket(data)
                self.writeQueue.join()
                info('Calling execute: {}'.format(commands[message['channel']]))
                output, result = executeCommand(commands[message['channel']])
                debug('ProcessPowerCommand: {}, result: {}, output: {}'.format(message, result, output))
                if result != 0:
                    error_message = 'Error executing shutdown command'
        except Exception as ex:
            error_message = '{}: {}'.format(type(ex).__name__, ex)
        if error_message:
            error(error_message)
            data = []
            cayennemqtt.DataChannel.add(data, message['channel'], value=0)
            self.EnqueuePacket(data)
            raise ExecuteMessageError(error_message)
        return error_message == None

    def ProcessAgentCommand(self, message):
        """Process command to manage the agent state

        Returns: True if command was processed, False otherwise."""
        error = None
        try:
            if message['suffix'] == 'uninstall':
                output, result = executeCommand('sudo -n /etc/myDevices/uninstall/uninstall.sh', disablePipe=True)
                debug('ProcessAgentCommand: {}, result: {}, output: {}'.format(message, result, output))
                if result != 0:
                    error = 'Error uninstalling agent'
            # elif message['suffix'] == 'config':
            #     for key, value in message['payload'].items():
            #         if value is None:
            #             info('Remove config item: {}'.format(key))
            #             self.config.remove('Agent', key)
            #         else:
            #             info('Set config item: {} {}'.format(key, value))
            #             self.config.set('Agent', key, value)
            else:
                error = 'Unknown agent command: {}'.format(message['suffix'])
        except Exception as ex:
            error = '{}: {}'.format(type(ex).__name__, ex)
        self.EnqueueCommandResponse(message, error)
        if error:
            raise ExecuteMessageError(error)
        return error == None

    def ProcessConfigCommand(self, message):
        """Process system configuration command

        Returns: True if command was processed, False otherwise."""
        error = None
        try:
            value = 1 - int(message['payload']) #Invert the value since the config script uses 0 for enable and 1 for disable
            command_id = {cayennemqtt.SYS_I2C: 11, cayennemqtt.SYS_SPI: 12, cayennemqtt.SYS_UART: 13, cayennemqtt.SYS_ONEWIRE: 19}
            result, output = SystemConfig.ExecuteConfigCommand(command_id[message['channel']], value)
            debug('ProcessConfigCommand: {}, result: {}, output: {}'.format(message, result, output))
            if result != 0:
                error = 'Error executing config command'
        except Exception as ex:
            error = '{}: {}'.format(type(ex).__name__, ex)
        self.EnqueueCommandResponse(message, error)
        return error == None

    def ProcessGpioCommand(self, message):
        """Process GPIO command

        Returns: True if command was processed, False otherwise."""
        error = None
        try:
            channel = int(message['channel'].replace(cayennemqtt.SYS_GPIO + ':', ''))
            result = 'ok'
            # result = self.sensorsClient.GpioCommand(message.get('suffix', 'value'), channel, message['payload'])
            debug('ProcessGpioCommand result: {}'.format(result))
            if result == 'failure':
                error = 'GPIO command failed'
        except Exception as ex:
            error = '{}: {}'.format(type(ex).__name__, ex)
        self.EnqueueCommandResponse(message, error)
        return error == None

    def ProcessSensorCommand(self, message):
        """Process sensor command

        Returns: True if command was processed, False otherwise."""
        error = None
        try:
            sensor_info = message['channel'].replace(cayennemqtt.DEV_SENSOR + ':', '').split(':')
            sensor = sensor_info[0]
            channel = None
            if len(sensor_info) > 1:
                channel = sensor_info[1]
            # result = self.sensorsClient.SensorCommand(message.get('suffix', 'value'), sensor, channel, message['payload'])
            result = 'ok'
            debug('ProcessSensorCommand result: {}'.format(result))
            if result is False:
                error = 'Sensor command failed'
        except Exception as ex:
            error = '{}: {}'.format(type(ex).__name__, ex)
        self.EnqueueCommandResponse(message, error)
        return error == None

    def ProcessDeviceCommand(self, message):
        """Process a device command to add/edit/remove a sensor

        Returns: True if command was processed, False otherwise."""
        error = None
        try:
            payload = message['payload']
            info('ProcessDeviceCommand payload: {}'.format(payload))
            # if message['suffix'] == 'add':
            #     result = self.sensorsClient.AddSensor(payload['sensorId'], payload['description'], payload['class'], payload['args'])
            # elif message['suffix'] == 'edit':
            #     result = self.sensorsClient.EditSensor(payload['sensorId'], payload['description'], payload['class'], payload['args'])
            # elif message['suffix'] == 'delete':
            #     result = self.sensorsClient.RemoveSensor(payload['sensorId'])
            # else:
            #     error = 'Unknown device command: {}'.format(message['suffix'])
            debug('ProcessDeviceCommand result: {}'.format(result))
            if result is False:
                error = 'Device command failed'
        except Exception as ex:
            error = '{}: {}'.format(type(ex).__name__, ex)
        self.EnqueueCommandResponse(message, error)
        return error == None

    def ProcessSchedulerCommand(self, message):
        """Process command to add/edit/remove a scheduled action

        Returns: True if command was processed, False otherwise."""
        error = None
        try:
            if message['suffix'] == 'add':
                result = self.schedulerEngine.add_scheduled_event(message['payload'], True)
            elif message['suffix'] == 'edit':
                result = self.schedulerEngine.update_scheduled_event(message['payload'])
            elif message['suffix'] == 'delete':
                result = self.schedulerEngine.remove_scheduled_event(message['payload'])
            elif message['suffix'] == 'get':
                events = self.schedulerEngine.get_scheduled_events()
                self.EnqueuePacket(events, cayennemqtt.JOBS_TOPIC)
            else:
                error = 'Unknown schedule command: {}'.format(message['suffix'])
            debug('ProcessSchedulerCommand result: {}'.format(result))
            if result is False:
                error = 'Schedule command failed'
        except Exception as ex:
            error = '{}: {}'.format(type(ex).__name__, ex)
        self.EnqueueCommandResponse(message, error)
        return error == None

    def EnqueueCommandResponse(self, message, error):
        """Send response after processing a command message"""
        if not 'cmdId' in message:
            # If there is no command id we assume this is a scheduled command and don't send a response message.
            return
        debug('EnqueueCommandResponse error: {}'.format(error))
        if error:
            response = 'error,{}={}'.format(message['cmdId'], error)
        else:
            response = 'ok,{}'.format(message['cmdId'])
        info(response)
        self.EnqueuePacket(response, cayennemqtt.COMMAND_RESPONSE_TOPIC)

    def EnqueuePacket(self, message, topic=cayennemqtt.DATA_TOPIC):
        """Enqueue a message packet to send to the server"""
        packet = (topic, message)
        self.writeQueue.put(packet)

    def DequeuePacket(self):
        """Dequeue a message packet to send to the server"""
        packet = (None, None)
        try:
            packet = self.writeQueue.get(False)
        except Empty:
            pass
        return packet

    # def SendHistoryData(self):
    #     """Enqueue a packet containing historical data to send to the server"""
    #     try:
    #         info('SendHistoryData start')
    #         history = History()
    #         history.Reset()
    #         while True:
    #             try:
    #                 #If there is no acknowledgment after a minute we assume failure
    #                 sendFailed = [key for key, item in self.sentHistoryData.items() if (item['Timestamp'] + 60) < time()]
    #                 info('SendHistoryData previously SendFailed items: ' + str(sendFailed))
    #                 for id in sendFailed:
    #                     self.historySendFails += len(sendFailed)
    #                     history.Sent(False, self.sentHistoryData[id]['HistoryData'])
    #                     del self.sentHistoryData[id]
    #                 historyData = history.GetHistoricalData()
    #                 if historyData:
    #                     data = {}
    #                     info('SendHistoryData historyData: ' + str(historyData))
    #                     data['MachineName'] = self.MachineId
    #                     data['Timestamp'] = int(time())
    #                     data['PacketType'] = PacketTypes.PT_HISTORY_DATA.value
    #                     id = sha256(dumps(historyData).encode('utf8')).hexdigest()
    #                     data['Id'] = id
    #                     data['HistoryData'] = historyData
    #                     info('Sending history data, id = {}'.format(id))
    #                     debug('SendHistoryData historyData: ' + str(data))
    #                     self.EnqueuePacket(data)
    #                     #this will keep accumulating
    #                     self.sentHistoryData[id] = data
    #             except Exception as ex:
    #                 exception('SendHistoryData error' + str(ex))
    #             delay = 60
    #             if self.historySendFails > 2:
    #                 delay = 120
    #             if self.historySendFails > 4:
    #                 #Wait an hour if we keep getting send failures.
    #                 delay = 3600
    #                 self.historySendFails = 0
    #             sleep(delay)
    #     except Exception as ex:
    #         exception('SendHistoryData general exception: ' + str(ex))
