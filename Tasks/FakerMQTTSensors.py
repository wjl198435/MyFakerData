import sys
sys.path.append("..")
from DBManager.createIOTables import getIotDataBaseSession,Sensor,Company,User,SensorInfo
from utils.logger import info, setInfo,debug,setDebug

#  mosquitto_pub -h 127.0.0.1 -p 1883 -t "homeassistant/sensor/temperature/room1_yancheng/config"  -m '{"device_class": "room1.temperature", "name": "room1.Temperature", "state_topic": "homeassistant/sensor/sensorBedroom/state", "unit_of_measurement": "°C", "value_template": "{{ value_json.temperature}}" }'
# mosquitto_pub -h 127.0.0.1 -p 1883 -t 'homeassistant/sensor/yancheng/room5/config' -m '{"device_class": "humidity", "name": "room5.Humidity1", "state_topic": "homeassistant/sensor/sensorBedroom/state", "unit_of_measurement": "%", "value_template": "{{ value_json.humidity}}" }'

class FakeMQSensors(object):
    def __init__(self, serverclient = None,session = None,company_id = 6):
        self.dbsession = session
        self._company_id = company_id
        self._serverclient = serverclient
        # self.cloudClient.EnqueuePacket(self.schedulerEngine.get_scheduled_events(),"test")


     #/* select  concat('room', FLOOR(1 + (RAND() * 10))); */
    def create_temperature_sensors(self):
        # sql = sensors = self.dbsession.query(SensorInfo.id,Sensor.domain,Sensor.unit,SensorInfo.mac,SensorInfo.loc). \
        #     join(SensorInfo). \
        #     filter(Sensor.company_id==str(self._company_id))
        # info(sql)
        # info(self._company_id)
        sensors = self.dbsession.query(SensorInfo.id,Sensor.domain,Sensor.unit,SensorInfo.mac,SensorInfo.loc).\
            join(SensorInfo).\
            filter(Sensor.company_id==str(self._company_id)).filter(Sensor.domain!='switch').all()


        users = self.dbsession.query(User.username,User.password).\
            filter(User.company_id==str(self._company_id)).first()

        topic = Sensor.domain

        for sensor in sensors:
            # SensorInfo.loc = 'room1'
            # debug(users)
            debug("sensor/{}/{}/{}/{}".format(sensor[1],sensor[4],users[0],users[1]))
        self.dbsession.commit()


if __name__ == '__main__':
    setDebug()
    session = getIotDataBaseSession
    MQSensors = FakeMQSensors(session=getIotDataBaseSession(),company_id=6)
    MQSensors.create_temperature_sensors()

