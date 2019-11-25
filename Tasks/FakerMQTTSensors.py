import sys
sys.path.append("..")
from DBManager.createIOTables import getIotDataBaseSession,Sensor,Company,User,SensorInfo
from utils.logger import info, setInfo,debug,setDebug
from config import MQTT_DIS_PREFIX
from Scheduler.scheduler import SchedulerEngine
import datetime

class FakeMQSensors(object):
    def __init__(self, serverclient = None,session = getIotDataBaseSession(),company_id = 6):
        self.dbsession = session
        self._company_id = company_id
        self._serverclient = serverclient
        self.sensors = None

        while self._serverclient.mqttClient.connected is False:
            pass
        self.add_temperature_sensors()

        self.schedulerEngine = SchedulerEngine(self, 'client_scheduler')

    def do_faker_sensor(self):
        debug("do_faker_sensor")

    def add_schedule_job(self):
        now = datetime.datetime.strftime(datetime.datetime.utcnow(), '%Y-%m-%dT%H:%M:%S.%fZ')
        event = {'id':'testSeconds', 'title':'faker_sensors_minute', 'actions':['self.do_faker_sensor'], 'config':{'type':'interval','unit':'minute', 'interval':5,'start_date':now}}
        self.schedulerEngine.add_scheduled_event(event, False)
        return event
     #/* select  concat('room', FLOOR(1 + (RAND() * 10))); */
    def add_temperature_sensors(self):

        self.sensors = self.dbsession.query(Sensor.domain,Sensor.sn,Sensor.unit,SensorInfo.loc,Company.english_name).\
            join(SensorInfo).join(Company).\
            filter(Sensor.company_id==str(self._company_id)).filter(Sensor.domain!='switch').filter(Sensor.domain!='fans').all()

        for sensor in self.sensors:
            sensor_topic = "sensor/{}/{}/config".format(sensor[-1],sensor.sn)
            sensor_config={
                "device_class": "temperature",
                "name": str(sensor.domain+"_"+sensor[3]),
                "state_topic": "{}/sensor/{}/{}/state".format(MQTT_DIS_PREFIX,sensor[-1],sensor.sn),
                "unit_of_measurement": sensor.unit,
                "value_template": "{{ value_json.temperature}}"
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
