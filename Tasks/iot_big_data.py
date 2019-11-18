# https://www.runoob.com/python3/python-mysql-connector.html

import sys
sys.path.append("..")
from config import DB_USER ,DB_PSD ,DB_HOST, DB_DATABASE ,DB_CHARSET
from config import IOT_BIG_DATA_USER ,IOT_BIG_DATA_PSD ,IOT_BIG_DATA_HOST,IOT_BIG_DATA_DATABASE ,IOT_BIG_DATA_CHARSET
import mysql.connector

from utils.logger import info, setInfo,error
import traceback


iot_bg_db = mysql.connector.connect(
    host=IOT_BIG_DATA_HOST,
    user=IOT_BIG_DATA_USER,
    passwd=IOT_BIG_DATA_PSD,
    database=IOT_BIG_DATA_DATABASE,
)

# 创建数据库
mycursor = iot_bg_db.cursor()
mycursor.execute("CREATE DATABASE If Not Exists "+ IOT_BIG_DATA_DATABASE)


# 创建表
# mydb = mysql.connector.connect(
#     host=IOT_BIG_DATA_HOST,
#     user=IOT_BIG_DATA_USER,
#     passwd=IOT_BIG_DATA_PSD,
#     database=IOT_BIG_DATA_DATABASE,
# )
#
# # 创建数据库
# mycursor = mydb.cursor()

def create_pigs_live_tables():
    mycursor.execute("CREATE TABLE If Not Exists  pigs_live(id BIGINT  AUTO_INCREMENT PRIMARY KEY,total BIGINT, time  DATETIME)")

#exapmle: insert into  pigs_live(total,time)  (select count(*)  ,join_date  from iot_db2.animals where id <100)
# select count(*)  ,date_format(join_date,'%Y-%m-%d') as jdate from iot_db2.animals join iot_db2.animalinfos on iot_db2.animalinfos.id = iot_db2.animals.id  where  iot_db2.animalinfos.health_status <>'死亡'
# group by jdate
# order by jdate

## 计数历史全量 存活数据

    count_pig_live_sql = "insert into  pigs_live(total,time) select count(*)  ,date_format(join_date,'%Y-%m-%d') as jdate " \
       "from iot_db2.animals join iot_db2.animalinfos on iot_db2.animalinfos.id = iot_db2.animals.id " \
       " where  iot_db2.animalinfos.health_status <>'死亡' group by jdate  order by jdate"

    info(count_pig_live_sql)
    info("正在执行-历史生猪存活数据统计....")
    try:
        mycursor.execute(count_pig_live_sql)
    except:
        error(count_pig_live_sql)
        error("Error: unable to fecth data:")
    iot_bg_db.commit()


def count_pigs_deed():
    ## 计数历史全量 死亡数据
    mycursor.execute("CREATE TABLE If Not Exists  pigs_deed(id BIGINT AUTO_INCREMENT PRIMARY KEY,total BIGINT, time  DATETIME)")
    count_pig_deed_sql = "insert into  pigs_deed(total,time) select count(*)  ,date_format(join_date,'%Y-%m-%d') as jdate " \
                     "from iot_db2.animals join iot_db2.animalinfos on iot_db2.animalinfos.id = iot_db2.animals.id " \
                     " where  iot_db2.animalinfos.health_status ='死亡' group by jdate  order by jdate"
    try:
        info(count_pig_deed_sql)
        info("正在执行-历史生猪死亡数据统计....")
        print(count_pig_deed_sql)
        mycursor.execute(count_pig_deed_sql)
    except:
        error(count_pig_deed_sql)
        error("Error: unable to fecth data:")

    iot_bg_db.commit()


def count_pigs_deed_map():
    ## 计数历史全量 死亡地理分布数据
    mycursor.execute("CREATE TABLE If Not Exists  pigs_deed_geo(id BIGINT AUTO_INCREMENT PRIMARY KEY,total BIGINT,lat FLOAT,lon FLOAT,province VARCHAR(10), time  DATETIME)")
    count_pig_deed_map_sql = "insert into pigs_deed_geo(total,lat,lon,province,time) " \
                             "SELECT  count(iot_db2.animalinfos.id) as value," \
                             "iot_db2.companies.lat  as latitude ," \
                             "iot_db2.companies.lon as longitude," \
                             "iot_db2.`companies`.`province`," \
                             "date_format(iot_db2.animalinfos.time,'%Y-%m-%d')  " \
                             "FROM (iot_db2.animals INNER JOIN iot_db2.companies ON iot_db2.animals.`company_id`=iot_db2.companies.id) " \
                             "INNER JOIN iot_db2.animalinfos ON iot_db2.animals.`animalinfo_id`=iot_db2.animalinfos.id " \
                             "where iot_db2.animalinfos.health_status ='死亡'  group by  `province` order by value ASC"
    try:
        info(count_pig_deed_map_sql)
        info("正在执行-生猪死亡地理位置数据统计....")
        print(count_pig_deed_map_sql)
        mycursor.execute(count_pig_deed_map_sql)
    except Exception as e:
        error(count_pig_deed_map_sql)
        error(str(e))

    iot_bg_db.commit()

if __name__ == '__main__':
    setInfo()
    count_pigs_deed_map()
    iot_bg_db.close()





