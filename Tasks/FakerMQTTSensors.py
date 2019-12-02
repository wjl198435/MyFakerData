import sys
sys.path.append("..")
from DBManager.createIOTables import Sensor,Company,User,SensorInfo
from utils.logger import info, setInfo,debug,setDebug
from config import MQTT_DIS_PREFIX
from Scheduler.scheduler import SchedulerEngine
import datetime
import random
from threading import Thread, Event
from time import strftime, localtime, tzset, time, sleep
from sqlalchemy import create_engine
from sqlalchemy.orm import  sessionmaker
from config import DB_URL
engine = create_engine(DB_URL)

from cloud.mqtt import CloudServerClient

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
    def __init__(self, serverclient = None,session = None,company_id = 6):
        self.dbsession = session
        self._company_id = company_id
        self._serverclient = serverclient
        self.sensors = None
        Session = sessionmaker(bind=engine)
        self.dbsession = Session()

        while self._serverclient.mqttClient.connected is False:
            pass

        # self.add_temperature_sensors()

        # self.schedulerEngine = SchedulerEngine(self, 'client_scheduler')
        #
        # self.add_schedule_job()
        # sensors = self.get_sensors()
        # self.add_sensors(sensors)
        self.do_add_sensors(company_english_name="qiangshen")
        TimerThread(self.do_faker_sensor_value, 180, initial_delay=5)


    def RunAction(self, action):
        debug('RunAction:' + action)
        self.get_sensors()
        eval(action)()
        return True

    def do_faker_sensor_value(self):
        debug("do_faker_sensor")
        # self.get_sensors()
        self.get_sensors_sql()
        # sub_sensors=np.random.choice(self.sensors,10,replace=False)
        # sub_sensors = random.choice(self.sensors)

        for i in range(len(self.sensors)) :
            # debug("do_faker_sensor:{}".format(i))
            sensor =  random.choice(self.sensors)
            faker_sensor_topic = "sensor/{}/{}/state".format(sensor[-1],sensor.sn)

            faker_sensor_message={"user":sensor[-1],"sn":sensor.sn,"domain":sensor.domain,"location":sensor[3]}
            if sensor.domain == "temperature":
                faker_sensor_message["value"] = round(random.uniform(-10,40) ,1)
            if sensor.domain == "humidity":
                faker_sensor_message["value"] = round(random.uniform(1,99) ,1)
            if sensor.domain == "aqi":
                faker_sensor_message["value"] = round(random.uniform(1,999) ,1)
            if sensor.domain == "luminance":
                faker_sensor_message["value"] =  round(random.uniform(1,4999) ,1)
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
        sensors = self.dbsession. \
                query(Sensor.domain,Sensor.sn,Sensor.unit,SensorInfo.loc,Company.english_name). \
                join(SensorInfo).join(Company). \
                filter(Sensor.company_id==str(self._company_id)). \
                filter(Sensor.domain!='switch').filter(Sensor.domain!='fans').order_by(Sensor.sn).all()
        self.sensors = sensors
                # filter(Sensor.domain!='switch').filter(Sensor.domain!='fans').order_by(Sensor.sn).limit(10).all()
        return sensors

    def get_sensors_sql(self):
        sensors = self.dbsession.execute("select *  from `sensorinfos` join sensors on sensors.`sensorinfo_id`=`sensorinfos`.id where company_id=6 and loc REGEXP '^house1[_]'").fetchall()
        return sensors

    def add_sensors(sensor,company_english_name):
        device_class="none"
        sensor_topic = "sensor/{}/{}/config".format(company_english_name,sensor.sn)
        if  sensor.domain == 'temperature' or sensor.domain == 'illuminance' or sensor.domain == 'humidity':
            device_class = sensor.domain.lower()
        elif sensor.domain == 'aqi':
            device_class = 'pressure'
        elif sensor.domain == 'NH3':
            device_class = 'power'

        sensor_config= \
            {
            "device_class": device_class,
            "name": str(sensor.loc+"_"+sensor.domain),
            "state_topic": "{}/sensor/{}/{}/state".format(MQTT_DIS_PREFIX,company_english_name,sensor.sn),
            "unit_of_measurement": sensor.unit,
            "value_template": "{{ value_json.value}}"
            }
        # message = {"name": "garden88", "device_class": "motion", "state_topic": "homeassistant/binary_sensor/garden/state"}

        debug("sensor_topic:{}".format(sensor_topic))
        debug("sensor_config:{}".format(sensor_config))
        return  sensor_topic,sensor_config

    def do_add_sensors(self,company_english_name):
        sensors = self.get_sensors_sql()
        for sensor in sensors:
            sensor_topic,sensor_config =  add_sensors(sensor,company_english_name)
            debug(sensor_topic)
            debug(sensor_config)
            self._serverclient.EnqueuePacket(sensor_config ,sensor_topic)

    # def add_sensors(self,sensors):
    #     # self.get_sensors()
    #     for sensor in sensors:
    #         sensor_topic = "sensor/{}/{}/config".format(sensor[-1],sensor.sn)
    #         if  sensor.domain == 'temperature' or sensor.domain == 'illuminance' or sensor.domain == 'humidity':
    #             device_class = sensor.domain.lower()
    #         elif sensor.domain == 'aqi':
    #             device_class = 'pressure'
    #         elif sensor.domain == 'NH3':
    #             device_class = 'power'
    #
    #         sensor_config=\
    #             {
    #             "device_class": device_class,
    #             "name": str(sensor[3]+"_"+sensor.domain),
    #             "state_topic": "{}/sensor/{}/{}/state".format(MQTT_DIS_PREFIX,sensor[-1],sensor.sn),
    #             "unit_of_measurement": sensor.unit,
    #             "value_template": "{{ value_json.value}}"
    #             }
    #         # message = {"name": "garden88", "device_class": "motion", "state_topic": "homeassistant/binary_sensor/garden/state"}
    #
    #         debug("sensor_topic:{}".format(sensor_topic))
    #         debug("sensor_config:{}".format(sensor_config))
    #
    #         self._serverclient.EnqueuePacket(sensor_config ,sensor_topic )
    #
    #     self.dbsession.commit()



def add_sensors(sensor,company_english_name):
    device_class="none"
    sensor_topic = "sensor/{}/{}/config".format(company_english_name,sensor.sn)
    if  sensor.domain == 'temperature' or sensor.domain == 'illuminance' or sensor.domain == 'humidity':
        device_class = sensor.domain.lower()
    elif sensor.domain == 'aqi':
        device_class = 'pressure'
    elif sensor.domain == 'NH3':
        device_class = 'power'

    sensor_config= \
            {
                "device_class": device_class,
                "name": str(sensor.loc+"_"+sensor.domain),
                "state_topic": "{}/sensor/{}/{}/state".format(MQTT_DIS_PREFIX,company_english_name,sensor.sn),
                "unit_of_measurement": sensor.unit,
                "value_template": "{{ value_json.value}}"
            }
        # message = {"name": "garden88", "device_class": "motion", "state_topic": "homeassistant/binary_sensor/garden/state"}

    # debug("sensor_topic:{}".format(sensor_topic))
    # debug("sensor_config:{}".format(sensor_config))
    return  sensor_topic,sensor_config

if __name__ == '__main__':
    setDebug()
    client = CloudServerClient("192.168.8.102", 1883, "192.168.8.102")
    Session = sessionmaker(bind=engine)
    session = Session()

    while client.mqttClient.connected is False:
        pass

    sensors = session.execute("select *  from `sensorinfos` join sensors on sensors.`sensorinfo_id`=`sensorinfos`.id where company_id=6 and loc REGEXP '^house1[_]'").fetchall()
    print(len(sensors))
    company_english_name = 'qiangshen'
    for sensor in sensors:
        # print(sensor.company_id)
        # topic,config = add_sensors(sensor)
        # client.mqtt_publish(topic,str(config))
        # client.EnqueuePacket(config ,topic )

        topic,config = add_sensors(sensor,company_english_name)
        client.mqtt_publish(topic,str(config))


    # MQSensors.create_temperature_sensors()
    #  mosquitto_pub -h 127.0.0.1 -p 1883 -t "homeassistant/sensor/temperature/room1_yancheng/config"  -m '{"device_class": "room1.temperature", "name": "room1.Temperature", "state_topic": "homeassistant/sensor/sensorBedroom/state", "unit_of_measurement": "°C", "value_template": "{{ value_json.temperature}}" }'
    #  mosquitto_pub -h 127.0.0.1 -p 1883 -t 'homeassistant/sensor/yancheng/room5/config' -m '{"device_class": "humidity", "name": "room5.Humidity1", "state_topic": "homeassistant/sensor/sensorBedroom/state", "unit_of_measurement": "%", "value_template": "{{ value_json.humidity}}" }'
    #  mosquitto_pub -h 127.0.0.1 -p 1883 -t 'homeassistant/sensor/qiangshen/737094851713/config' -m '{"device_class": "temperature", "name": "luminance_room10", "state_topic": "homeassistant/sensor/luminance/qiangshen/681810996134/state", "unit_of_measurement": "lu", "value_template": "{{ value_json.temperature}}"}'
    #  mosquitto_pub -h 127.0.0.1 -p 1883 -t 'homeassistant/sensor/user29/975782544212/config' -m '{"device_class": "humidity", "name": "room29.Humidity", "state_topic": "homeassistant/sensor/sensorBedroom/state", "unit_of_measurement": "%", "value_template": "{{ value_json.humidity}}" }'


# cards:
# - cards:
# - entity: sensor.house1_room10_temperature
# type: sensor
# - entity: sensor.house1_room15_humidity
# type: sensor
# - entity: sensor.house1_room13_illuminance
# type: sensor
# - entity: sensor.house1_room15_aqi
# type: sensor
# - entity: sensor.house1_room14_nh3_2
# type: sensor
# title: Lights
# type: horizontal-stack
# - aspect_ratio: 65%
# camera_image: camera.zi_tai_jian_ce
# camera_view: live
# entities:
# - entity: fan.mqtt_fan
# - entity: switch.demo_switch
# entity: camera.zi_tai_jian_ce
# image: 'https://www.home-assistant.io/images/merchandise/shirt-frontpage.png'
# type: picture-glance
# - aspect_ratio: 65%
# camera_image: camera.mu_biao_jian_ce
# camera_view: live
# entities:
# - entity: fan.mqtt_fan
# - entity: switch.demo_switch
# entity: camera.mu_biao_jian_ce
# image: 'https://www.home-assistant.io/images/merchandise/shirt-frontpage.png'
# type: picture-glance