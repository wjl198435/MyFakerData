import sys
sys.path.append("..")
from DBManager.createIOTables import getIotDataBaseSession,Sensor,Company,User,SensorInfo
from utils.logger import info, setInfo,debug,setDebug
class FakeMQSensors(object):
    def __init__(self, serverclient = None,session = None,company_id = 6):
        self.dbsession = session
        self._company_id = company_id


    def create_temperature_sensors(self):
        sensors = self.dbsession.query(Sensor.domain,Sensor.unit,SensorInfo.mac).join(SensorInfo).filter(Sensor.company_id==str(self._company_id)).all()
        users = self.dbsession.query(User.username,User.password).filter(User.company_id==str(self._company_id)).first()

        # debug(sensors)
        # debug(users)
        # debug("sensors:"+str(len(sensors)))
        # debug("users:"+str(len(users)))

        for sensor in sensors:
            debug(sensor)



if __name__ == '__main__':
    setDebug()
    session = getIotDataBaseSession
    MQSensors = FakeMQSensors(session=getIotDataBaseSession(),company_id=60)
    MQSensors.create_temperature_sensors()

