# coding: utf-8
from faker import Faker
import json
f = Faker(locale='zh_CN')

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, Integer

engine = create_engine('mysql+pymysql://hass:hass@192.168.8.102/watch_dog_db?charset=utf8')
Base = declarative_base()

class User(Base):

    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    username = Column(String(64), nullable=False, index=True)
    password = Column(String(64), nullable=False)
    email = Column(String(64), nullable=False, index=True)


    def __repr__(self):
        return '%s(%r)' % (self.__class__.__name__, self.username)

sensor_type = ("temp", "humi", "light", "aqi")
sensor_unit_list = ('℃', 'rh%', 'lum', 'ug')
sensor_range_min = (-50, 0, 0, 0)
sensor_range_max = (50, 100, 10000, 5000)

def fake_sensor_data(clientid,user_name,sensor_type='temp',unit='℃',min=0,max=100):
    temp = {
        'username': user_name,
        'clientid': clientid,
        'company': f.company_prefix(),
        'type': sensor_type,
        'value': f.random_int(min=min, max=max),
        'uptime': f.unix_time(),
        'unit': unit,
        'mac': f.mac_address(),
        'isbn': f.isbn10(), #设备编号
        "geo": {
            "key": "zh_CN",
            "latitude": float(f.latitude()),
            "longitude": float(f.longitude()),
            "name": "中国",
        },
    }

    json_str = json.dumps(temp)
    return json_str





if __name__ == '__main__':
    # user = User()
    print(str(User))