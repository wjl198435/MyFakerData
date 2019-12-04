import sys
sys.path.append("..")
from DBManager.createIOTables import Sensor,Company,User,SensorInfo
from utils.logger import info, setInfo,debug,setDebug
from config import MQTT_DIS_PREFIX,MQTT_CLIENT_ID
from Scheduler.scheduler import SchedulerEngine
import datetime
import random
from threading import Thread, Event
from time import strftime, localtime, tzset, time, sleep
from sqlalchemy import create_engine
from sqlalchemy.orm import  sessionmaker
from config import DB_URL
engine = create_engine(DB_URL)

from utils.logger import info, setInfo,debug

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
        self.sensors = []
        self.switches = []
        self.lights = []
        self.climates = []
        self.fans = []
        Session = sessionmaker(bind=engine)
        self.dbsession = Session()

        while self._serverclient.mqttClient.connected is False:
            pass


        # self.schedulerEngine = SchedulerEngine(self, 'client_scheduler')
        # self.add_schedule_job()

        # # add  mqtt sensors
        # domain = 'sensor'
        # self.sensors = self.get_device_from_db(domain)
        # self.do_add_mqtt_sensors(mqtt_client_id=MQTT_CLIENT_ID)
        #
        #
        # # add mqtt switch
        # domain = 'switch'
        # self.switches = self.get_device_from_db(domain)
        # debug("self.switches={}".format(len(self.switches)))
        # self.do_add_mqtt_switch(mqtt_client_id=MQTT_CLIENT_ID)

        # # add mqtt light
        # domain = 'light'
        # self.lights = self.get_device_from_db(domain)
        # debug("self.lights={}".format(len(self.lights)))
        # self.do_add_mqtt_lights(mqtt_client_id=MQTT_CLIENT_ID)
        #
        # # add mqtt climate
        # domain = 'climate'
        # self.climates = self.get_device_from_db(domain)
        # debug("self.climate={}".format(len(self.climates)))
        # self.do_add_mqtt_climates(mqtt_client_id=MQTT_CLIENT_ID)


        # add mqtt climate
        domain = 'fan'
        self.fans = self.get_device_from_db(domain)
        debug("self.fan={}".format(len(self.fans)))
        self.do_add_mqtt_fans(mqtt_client_id=MQTT_CLIENT_ID)

        TimerThread(self.do_faker_sensor_value, 180, initial_delay=5)


    def RunAction(self, action):
        debug('RunAction:' + action)
        # domain = 'sensor'
        self.get_device_from_db()
        eval(action)()
        return True

    def do_faker_sensor_value(self,mqtt_client_id=MQTT_CLIENT_ID):
        debug("do_faker_sensor")
        # self.get_sensors_sql()
        for sensor in  self.sensors :

            faker_sensor_topic = "sensor/{}/{}/state".format(mqtt_client_id,sensor.loc+"_"+sensor.device_class)

            faker_sensor_message={"user":MQTT_CLIENT_ID,"sn":sensor.sn,"domain":sensor.domain,"device_class":sensor.device_class,"location":sensor.loc}
            if sensor.device_class == "temperature":
                faker_sensor_message["value"] = round(random.uniform(-10,40) ,1)
            elif sensor.device_class == "humidity":
                faker_sensor_message["value"] = round(random.uniform(1,99) ,1)
            elif sensor.device_class == "pm25":
                faker_sensor_message["value"] = round(random.uniform(1,999) ,1)
            elif sensor.device_class == "illuminance":
                faker_sensor_message["value"] =  round(random.uniform(1,4999) ,1)
            if sensor.device_class == "nh3":
                faker_sensor_message["value"]  = round(random.uniform(1,999) ,1)

            self._serverclient.EnqueuePacket(faker_sensor_message ,faker_sensor_topic)


    def add_schedule_job(self):
        now = datetime.datetime.strftime(datetime.datetime.utcnow(), '%Y-%m-%dT%H:%M:%S.%fZ')
        event = {'id':'faker_sensor', 'title':'faker_sensors_minute', 'actions':['self.do_faker_sensor'], 'config':{'type':'interval','unit':'second', 'interval':300,'start_date':now}}
        self.schedulerEngine.add_scheduled_event(event)
        return event
     #/* select  concat('room', FLOOR(1 + (RAND() * 10))); */

    def get_device_from_db(self,domain='sensor'):
        deivces = self.dbsession. \
                query(Sensor.domain,Sensor.device_class,Sensor.sn,Sensor.unit,SensorInfo.loc). \
                join(SensorInfo).join(Company). \
                filter(Sensor.company_id==str(self._company_id)). \
                filter(Sensor.domain==domain).order_by(Sensor.sn).all()
        return deivces

    def get_sensors_sql(self):
        sensors = self.dbsession.execute("select *  from `sensorinfos` join sensors on sensors.`sensorinfo_id`=`sensorinfos`.id where company_id=6 and domain='sensor'  and loc REGEXP '^house1[_]'").fetchall()
        self.sensors=sensors
        return sensors

    def add_mqtt_sensor_devices(self, sensor, mqtt_client_id='qiangshen'):
        device_class="none"
        unit = "℃"
        # sensor_topic = "sensor/{}/{}/config".format(mqtt_client_id,sensor.sn)
        sensor_topic = "sensor/{}/{}/config".format(mqtt_client_id,sensor.loc+"_"+sensor.device_class)
        if sensor.device_class == "nh3":
            device_class = 'power'
        elif sensor.device_class == 'pm25':
            device_class = 'pressure'
        else:
            device_class = sensor.device_class
        sensor_config= \
            {
            "device_class": device_class,
            "name": str(sensor.loc)+"_"+sensor.device_class,
            "state_topic": "{}/sensor/{}/{}/state".format(MQTT_DIS_PREFIX,mqtt_client_id,sensor.loc+"_"+sensor.device_class),
            "unit_of_measurement": sensor.unit,
            "value_template": "{{ value_json.value}}"
            }

        # debug("sensor_topic:{}".format(sensor_topic))
        # debug("sensor_config:{}".format(sensor_config))
        return  sensor_topic,sensor_config

    def do_add_mqtt_switch(self, mqtt_client_id=""):
        _switchs = self.switches
        for switch in _switchs:
            switch_topic = "switch/{}/{}/config".format(mqtt_client_id,switch.loc + "_"+ switch.device_class)
            switch_config =\
                {
                 "~": "homeassistant/switch/{}/{}".format(mqtt_client_id,switch.loc + "_"+ switch.device_class),
                 "name": "{}".format(switch.loc )+"_"+sensor.device_class,
                 "cmd_t": "~/set",
                 "stat_t": "~/state",
                 "payload_on": "1",
                 "payload_off": "0",
                 "value_template": '{{value_json.on}}'
                }
            debug(switch_topic)
            debug(switch_config)
            # sensor_topic,sensor_config =  self.add_mqtt_sensor_devices(sensor, mqtt_client_id)
            self._serverclient.EnqueuePacket(switch_config ,switch_topic)


    def do_add_mqtt_lights(self, mqtt_client_id=""):
        _lights = self.lights
        for light in _lights:
            light_topic = "light/{}/{}/config".format(mqtt_client_id,light.loc + "_"+ light.device_class)
            light_config = \
                {
                    "~": "homeassistant/light/{}/{}".format(mqtt_client_id,light.loc + "_"+ light.device_class),
                    "name": "{}".format(light.loc),
                    "cmd_t": "~/set",
                    "stat_t": "~/state",
                    "payload_on": "1",
                    "payload_off": "0",
                    "value_template": '{{value_json.on}}'
                }
            debug(light_topic)
            debug(light_config)
            # sensor_topic,sensor_config =  self.add_mqtt_sensor_devices(sensor, mqtt_client_id)
            self._serverclient.EnqueuePacket(light_config ,light_topic)

    def do_add_mqtt_fans(self, mqtt_client_id=""):
        #
        # payload { "speed": "low"}
        # payload  { "state": "low"}
        _fans = self.fans
        for fan in _fans[0:2]:
            fan_topic = "fan/{}/{}/config".format(mqtt_client_id,fan.loc + "_"+ fan.device_class)
            fan_config = \
                {
                    "~": "homeassistant/fan/{}/{}".format(mqtt_client_id,fan.loc + "_"+ fan.device_class),
                    "name": "{}".format(fan.loc),
                    "cmd_t": "~/set",
                    "stat_t": "~/state",
                    "pl_on": "on",
                    "pl_off": "off",
                    "stat_val_tpl": '{{value_json.state}}',
                    "spd_stat_t": "~/state",
                    "spd_cmd_t": "~/set",
                    "spds": ["off","low","medium","high"],
                    "spd_val_tpl": '{{value_json.speed}}',
                    "qos": "0"
                }
            debug(fan_topic)
            debug(fan_config)
            # sensor_topic,sensor_config =  self.add_mqtt_sensor_devices(sensor, mqtt_client_id)
            self._serverclient.EnqueuePacket(fan_config ,fan_topic)



    def do_add_mqtt_climates(self, mqtt_client_id=""):
        _climates = self.climates
        for climate in _climates:
            climate_topic = "climate/{}/{}/config".format(mqtt_client_id,climate.loc + "_"+ climate.device_class)

            # State payload
            # {
            #     "mode":"off",
            #     "target_temp":"21.50",
            #     "current_temp":"23.60",
            # }
            climate_config = \
                {
                    "~": "homeassistant/climate/{}/{}".format(mqtt_client_id,climate.loc),
                    "name": "{}".format(climate.loc),
                    "mode_cmd_t": "~/set",
                    "mode_stat_t": "~/state",
                    "mode_stat_tpl":"",
                    "avty_t":"~/available",
                    "pl_avail":"online",
                    "payload_on": "1",
                    "pl_not_avail":"offline",
                    "temp_cmd_t":"~/targetTempCmd",
                    "temp_stat_t":"~/state",
                    "curr_temp_t":"~/state",
                    "curr_temp_tpl":"",
                    "curr_temp_tpl":"",
                    "min_temp":"15",
                    "max_temp":"25",
                    "temp_step":"0.5",
                    "modes":["off","cool","fan_only" ,'auto',"dry","heat"]
                }



            debug(climate_topic)
            debug(climate_config)
            # sensor_topic,sensor_config =  self.add_mqtt_sensor_devices(sensor, mqtt_client_id)
            self._serverclient.EnqueuePacket(climate_config ,climate_topic)




    def do_add_mqtt_sensors(self, mqtt_client_id=""):
        _sensors = self.sensors
        for sensor in _sensors:
            sensor_topic,sensor_config =  self.add_mqtt_sensor_devices(sensor, mqtt_client_id)
            self._serverclient.EnqueuePacket(sensor_config ,sensor_topic)



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