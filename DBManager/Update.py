import datetime
import time
from sqlalchemy import create_engine
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy import text

import sys
sys.path.append("..")

import random
from createTables import Company,AnimalInfo,Sensor,Camera

from config import DB_URL
from utils.city2lnglat import address2latlng

database = 'iot_db2'
engine = create_engine(DB_URL.format(database))

# Session = sessionmaker(bind=engine)
# session = Session()

Session = sessionmaker(bind=engine)
session = Session()

def update_latlng_from_address():

    # 三张表关联 SELECT * FROM (表1 INNER JOIN 表2 ON 表1.字段号=表2.字段号) INNER JOIN 表3 ON 表1.字段号=表3.字段号
    # SELECT * FROM (animals INNER JOIN companies ON animals.`company_id`=companies.id) INNER JOIN animalinfos ON animals.`animalinfo_id`=animalinfos.id where animals.id<100  limit 100

    print("update_latlng_from_address")
    for animalinfo in session.query(AnimalInfo).filter(AnimalInfo.id <1000):
        print(animalinfo.address)
        result = address2latlng(animalinfo.address)
        print(result)
        # print(ani.address)
    session.commit()

def get_company_id():
    companies_id = []
    for company in session.query(Company.id).all():
        companies_id.append(company.id)
    return  companies_id

def update_sensor_company_id(Table):
    i = 0
    # print(session.query(Table).filter(text("company_id = NULL")))
    for sensor in session.query(Table).filter(text("ISNULL(sensors.company_id)")):
        # print("sensor.id={} ,{} get_company_id:{}".format(str(random.choice(get_company_id()))))
        # print(sensor.company_id)
        sensor.company_id = random.choice(get_company_id())
        i+=1
        if i%500 == 0:
            print("commit:{}  id={}".format(i,sensor.id))
            session.commit()
    # pass
    session.commit()

def update_camera_company_id(Table):
    i = 0
    # print(session.query(Table).filter(text("company_id = NULL")))
    for sensor in session.query(Table).filter(text("ISNULL(cameras.company_id)")):
        # print("sensor.id={} ,{} get_company_id:{}".format(str(random.choice(get_company_id()))))
        # print(sensor.company_id)
        sensor.company_id = random.choice(get_company_id())
        i+=1
        if i%500 == 0:
            print("{} commit:{}  id={}".format("camera",i,sensor.id))
            session.commit()
    # pass
    session.commit()
    # 三张表关联 SELECT * FROM (表1 INNER JOIN 表2 ON 表1.字段号=表2.字段号) INNER JOIN 表3 ON 表1.字段号=表3.字段号
    # SELECT * FROM (animals INNER JOIN companies ON animals.`company_id`=companies.id) INNER JOIN animalinfos ON animals.`animalinfo_id`=animalinfos.id where animals.id<100  limit 100
    # company_id,_ = session.query(Company.id)
    # for company in session.query(Company.id).all():
    #     print(company.id)


    # print("update_latlng_from_address")
    # for animalinfo in session.query(Sensor):
    #     print(animalinfo.address)
    #     result = address2latlng(animalinfo.address)
    #     print(result)
    #     # print(ani.address)
    # session.commit()

if __name__ == '__main__':

    # update_latlng_from_address()
    # update_sensor_company_id(Sensor)
    update_camera_company_id(Camera)
    # print(random.choice(get_company_id()))

    session.close()
    # for com in session.query(Company):
    #     result = address2latlng(com.province)
    #     # print(result)
    #     if result['status'] ==0:
    #         lng = result["result"]["location"]["lng"]
    #         lat = result["result"]["location"]["lat"]
    #         print(lng,lat)
    #         com.lat = lat
    #         com.lon = lng
    #
    # session.commit()
