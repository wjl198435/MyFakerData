import datetime
import time
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy import Column, String, Integer, Text, ForeignKey, Table, DateTime, FLOAT, Text,Time
import random
from dbManager import Company

from config import DB_URL
from city2lnglat import address2latlng

database = 'iot_db2'
engine = create_engine(DB_URL.format(database))

if __name__ == '__main__':
    Session = sessionmaker(bind=engine)
    session = Session()
    for com in session.query(Company):
        result = address2latlng(com.province)
        # print(result)
        if result['status'] ==0:
            lng = result["result"]["location"]["lng"]
            lat = result["result"]["location"]["lat"]
            print(lng,lat)
            com.lat = lat
            com.lon = lng

    session.commit()
        # print(address2latlng(com.city))
        # print(type(result))
        #
        # if result["status"] == 0:
        #     print(result["result"]["location"])


        # print(com)
    # with session.begin():
    #     a = session.query(Company).get(10)
    #     print(a)




#     /* CREATE TABLE `worldmap_latlng` (
#         `id` int(11) NOT NULL AUTO_INCREMENT,
#                               `lat` FLOAT NOT NULL,
#                                               `lng` FLOAT NOT NULL,
#                                                               `name` VARCHAR(20) NOT NULL,
#                                                                                      `value` FLOAT NOT NULL,
#                                                                                                        `timestamp` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
#                                                                                                                                                                           PRIMARY KEY (`id`)
#     ) AUTO_INCREMENT=7 DEFAULT CHARSET=latin1;
# */
#
# /* INSERT INTO `worldmap_latlng`
# (`lat`,
#  `lng`,
#  `name`,
#  `value`,
#  `timestamp`)
# VALUES
# (39.234,
#  116.3234,
#  'Beijing',
#  1.0,
#  now()); */
#
# /* INSERT INTO `worldmap_latlng`
# (`lat`,
#  `lng`,
#  `name`,
#  `value`,
#  `timestamp`)
# VALUES
# (34.234,
#  121.3234,
#  'Shanghai',
#  3.0,
#  now()); */
#
# /* INSERT INTO  `worldmap_latlng`
# (`lat`,
#  `lng`,
#  `name`,
#  `value`,
#  `timestamp`)
# VALUES
# (39.234,
#  121.3234,
#  'Tianjing',
#  5.23,
#  now()); */
# /*
# SELECT
# `scale` as value,
# `lat` as latitude,
# `lon` as longitude,
# `city` as name
# FROM companies */
#
#
# SELECT
# `scale` as value,
# `lat` as latitude,
# `lon` as longitude,
# `province` as name
# FROM companies
# group by  `province`
# order by value ASC