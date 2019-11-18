import datetime
import time
from sqlalchemy import create_engine
from sqlalchemy.orm import relationship, sessionmaker

import sys
sys.path.append("..")

import random
from createTables import Company,AnimalInfo

from config import DB_URL
from utils.city2lnglat import address2latlng

database = 'iot_db2'
engine = create_engine(DB_URL.format(database))

# Session = sessionmaker(bind=engine)
# session = Session()

def update_latlng_from_address():

    # 三张表关联 SELECT * FROM (表1 INNER JOIN 表2 ON 表1.字段号=表2.字段号) INNER JOIN 表3 ON 表1.字段号=表3.字段号
    # SELECT * FROM (animals INNER JOIN companies ON animals.`company_id`=companies.id) INNER JOIN animalinfos ON animals.`animalinfo_id`=animalinfos.id where animals.id<100  limit 100
    Session = sessionmaker(bind=engine)
    session = Session()
    print("update_latlng_from_address")
    for animalinfo in session.query(AnimalInfo).filter(AnimalInfo.id <1000):
        print(animalinfo.address)
        result = address2latlng(animalinfo.address)
        print(result)
        # print(ani.address)
    session.commit()

if __name__ == '__main__':

    update_latlng_from_address()
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
