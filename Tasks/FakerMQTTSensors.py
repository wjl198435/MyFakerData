import sys
sys.path.append("..")
from DBManager.createIOTables import getIotDataBaseSession,Sensor,Company,User,SensorInfo
from utils.logger import info, setInfo,debug,setDebug
from config import MQTT_DIS_PREFIX
from Scheduler.scheduler import SchedulerEngine
import datetime
import random
from threading import Thread, Event
from time import strftime, localtime, tzset, time, sleep



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

class FakeMQSensors(object):
    def __init__(self, serverclient = None,session = getIotDataBaseSession(),company_id = 6):
        self.dbsession = session
        self._company_id = company_id
        self._serverclient = serverclient
        self.sensors = None

        while self._serverclient.mqttClient.connected is False:
            pass

        # self.add_temperature_sensors()

        # self.schedulerEngine = SchedulerEngine(self, 'client_scheduler')
        #
        # self.add_schedule_job()

        self.add_sensors()
        TimerThread(self.do_faker_sensor,5, initial_delay=5)


    def RunAction(self, action):
        debug('RunAction:' + action)
        self.get_sensors()
        eval(action)()
        return True

    def do_faker_sensor(self):
        debug("do_faker_sensor")
        self.get_sensors()
        # sub_sensors=np.random.choice(self.sensors,10,replace=False)
        # sub_sensors = random.choice(self.sensors)

        for i in range(10) :
            # debug("do_faker_sensor:{}".format(i))
            sensor =  random.choice(self.sensors)
            faker_sensor_topic = "sensor/{}/{}/state".format(sensor[-1],sensor.sn)

            faker_sensor_message={"user":sensor[-1],"sn":sensor.sn,"domain":sensor.domain,"location":sensor[3]}
            if sensor.domain == "temperature":
                faker_sensor_message["value"] = round(random.uniform(10,40) ,1)
            if sensor.domain == "humidity":
                faker_sensor_message["value"] = round(random.uniform(1,99) ,1)
            if sensor.domain == "aqi":
                faker_sensor_message["value"] = round(random.uniform(1,1999) ,1)
            if sensor.domain == "luminance":
                faker_sensor_message["value"] =  round(random.uniform(1,49999) ,1)
            if sensor.domain == "NH3":
                faker_sensor_message["value"]  = round(random.uniform(1,999) ,1)

            self._serverclient.EnqueuePacket(faker_sensor_message ,faker_sensor_topic)


    def add_schedule_job(self):
        now = datetime.datetime.strftime(datetime.datetime.utcnow(), '%Y-%m-%dT%H:%M:%S.%fZ')
        event = {'id':'faker_sensor', 'title':'faker_sensors_minute', 'actions':['self.do_faker_sensor'], 'config':{'type':'interval','unit':'second', 'interval':300,'start_date':now}}
        self.schedulerEngine.add_scheduled_event(event)
        return event
     #/* select  concat('room', FLOOR(1 + (RAND() * 10))); */

    def get_sensors(self):
        if self.sensors is None:
            self.sensors = self.dbsession. \
                query(Sensor.domain,Sensor.sn,Sensor.unit,SensorInfo.loc,Company.english_name). \
                join(SensorInfo).join(Company). \
                filter(Sensor.company_id==str(self._company_id)). \
                filter(Sensor.domain!='switch').filter(Sensor.domain!='fans').all()


    def add_sensors(self):
        self.get_sensors()
        for sensor in self.sensors:
            sensor_topic = "sensor/{}/{}/config".format(sensor[-1],sensor.sn)
            sensor_config=\
                {
                "device_class": "temperature",
                "name": str(sensor[3]+"_"+sensor.domain),
                "state_topic": "{}/sensor/{}/{}/state".format(MQTT_DIS_PREFIX,sensor[-1],sensor.sn),
                "unit_of_measurement": sensor.unit,
                "value_template": "{{ value_json.value}}"
                }
            # message = {"name": "garden88", "device_class": "motion", "state_topic": "homeassistant/binary_sensor/garden/state"}

            debug("sensor_topic:{}".format(sensor_topic))
            debug("sensor_config:{}".format(sensor_config))

            self._serverclient.EnqueuePacket(sensor_config ,sensor_topic )

        self.dbsession.commit()


if __name__ == '__main__':
    setDebug()
    session = getIotDataBaseSession
    MQSensors = FakeMQSensors(session=getIotDataBaseSession(),company_id=6)
    MQSensors.create_temperature_sensors()
    #  mosquitto_pub -h 127.0.0.1 -p 1883 -t "homeassistant/sensor/temperature/room1_yancheng/config"  -m '{"device_class": "room1.temperature", "name": "room1.Temperature", "state_topic": "homeassistant/sensor/sensorBedroom/state", "unit_of_measurement": "°C", "value_template": "{{ value_json.temperature}}" }'
    #  mosquitto_pub -h 127.0.0.1 -p 1883 -t 'homeassistant/sensor/yancheng/room5/config' -m '{"device_class": "humidity", "name": "room5.Humidity1", "state_topic": "homeassistant/sensor/sensorBedroom/state", "unit_of_measurement": "%", "value_template": "{{ value_json.humidity}}" }'
    #  mosquitto_pub -h 127.0.0.1 -p 1883 -t 'homeassistant/sensor/qiangshen/737094851713/config' -m '{"device_class": "temperature", "name": "luminance_room10", "state_topic": "homeassistant/sensor/luminance/qiangshen/681810996134/state", "unit_of_measurement": "lu", "value_template": "{{ value_json.temperature}}"}'
    #  mosquitto_pub -h 127.0.0.1 -p 1883 -t 'homeassistant/sensor/user29/975782544212/config' -m '{"device_class": "humidity", "name": "room29.Humidity", "state_topic": "homeassistant/sensor/sensorBedroom/state", "unit_of_measurement": "%", "value_template": "{{ value_json.humidity}}" }'
