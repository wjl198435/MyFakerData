# https://www.runoob.com/python3/python-mysql-connector.html

import sys
sys.path.append("..")
from config import DB_USER ,DB_PSD ,DB_HOST, DB_DATABASE ,DB_CHARSET
from config import BIG_DATA_USER ,BIG_DATA_PSD ,BIG_DATA_HOST,BIG_DATA_DATABASE ,BIG_DATA_CHARSET,BD_DATA_URL
import mysql.connector

from utils.logger import info, setInfo,error,debug,setDebug
import traceback

import datetime
import time
import datetime
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy import Column, String, Integer, ForeignKey, Table, DateTime, FLOAT, Text,Time,Date

Base = declarative_base()
engine = create_engine(BD_DATA_URL)

Session = sessionmaker(bind=engine)
session = Session()

iot_bg_db = mysql.connector.connect(
    host=BIG_DATA_HOST,
    user=BIG_DATA_USER,
    passwd=BIG_DATA_PSD,
)

# 创建数据库
mycursor = iot_bg_db.cursor()
mycursor.execute("CREATE DATABASE If Not Exists "+ BIG_DATA_DATABASE)
mycursor.execute("use "+BIG_DATA_DATABASE)

class PigPriceTable(Base):

    __tablename__ = 'PigPriceTable'

    id = Column(Integer, primary_key=True,index=True)
    省份 = Column(String(10))
    外三元 =  Column(FLOAT)
    内三元 =  Column(FLOAT)
    土杂猪 =  Column(FLOAT)
    日期 = Column(Date, nullable=False)
    time = Column(DateTime, nullable=False,default=datetime.datetime.utcnow,onupdate=datetime.datetime.utcnow)
    def __repr__(self):
        return '%s(%r) %s' % (self.__class__.__name__, self.日期,self.省份)

def pigPriceIsExist(day):
    sql = session.query(PigPriceTable).filter_by(日期 = str(day))
    debug(sql)
    result = sql.first()
    if result is None:
        return False
    else:
        return True

def test_pig_price_latest_date():

    # debug(datetime.date.today()- datetime.timedelta(days=+1))
    today = datetime.date.today()- datetime.timedelta(days=1)
    debug(today)
    print(pigPriceIsExist(str(today)))

class PigsLiveTable(Base):
    __tablename__ = 'PigsLiveTable'
    id = Column(Integer, primary_key=True,index=True)
    total = Column(Integer)
    time = Column(DateTime, nullable=False,default=datetime.datetime.utcnow,onupdate=datetime.datetime.utcnow)

class PigsDeedTable(Base):
    __tablename__ = 'PigsDeedTable'
    id = Column(Integer, primary_key=True,index=True)
    total = Column(Integer)
    time = Column(DateTime, nullable=False,default=datetime.datetime.now(),onupdate=datetime.datetime.utcnow)
    lat =  Column(FLOAT)
    lon =Column(FLOAT)
    province = Column(String(10))
    company = Column(String(50))
    company_id = Column(Integer)

def getBigDataBaseSession():
    Session = sessionmaker(bind=engine)
    session = Session()
    return session

def create_pigs_live_tables():
    mycursor.execute("CREATE TABLE If Not Exists  pigs_live(id BIGINT  AUTO_INCREMENT PRIMARY KEY,total BIGINT, time  DATETIME)")
    mycursor.execute("trucate pigs_live")


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
    mycursor.execute("trucate pigs_deed")
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
    mycursor.execute("trucate pigs_deed_geo")
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

def create_pigs_deed_geo():
    ## 计数历史全量 死亡地理分布数据
    mycursor.execute("CREATE TABLE If Not Exists  pigs_deed_geo(id BIGINT AUTO_INCREMENT PRIMARY KEY,total BIGINT,lat FLOAT,lon FLOAT,province VARCHAR(10), time  DATETIME)")
    iot_bg_db.commit()

def create_pigs_deed_table():
    mycursor.execute("CREATE TABLE If Not Exists  pigs_deed(id BIGINT AUTO_INCREMENT PRIMARY KEY,total BIGINT, time  DATETIME)")
    iot_bg_db.commit()
def create_pigs_live_table():
    mycursor.execute("CREATE TABLE If Not Exists  pigs_live(id BIGINT  AUTO_INCREMENT PRIMARY KEY,total BIGINT, time  DATETIME)")
    iot_bg_db.commit()
def create_pig_price_table():
    mycursor.execute("CREATE TABLE If Not Exists  pig_price(id BIGINT  AUTO_INCREMENT PRIMARY KEY,省份 VARCHAR(10), 外三元 FLOAT,内三元 FLOAT,土杂猪 FLOAT,日期 DATE ,time  DATETIME  NOT NULL DEFAULT '2019-00-00 00:00:00' ON UPDATE current_timestamp())")
    iot_bg_db.commit()

def create_database(database_name):
    mycursor.execute("CREATE DATABASE If Not Exists "+ database_name )

def create_bg_tables(database_name):
    try:
        create_database(database_name)
        create_pig_price_table()
        create_pigs_live_table()
        create_pigs_deed_table()
        create_pigs_deed_geo()
        iot_bg_db.close()
    except Exception as e:
        error(count_pig_deed_map_sql)
        error(str(e))

if __name__ == '__main__':
    setDebug()

    #更新动物活动时间
    # update `animalinfos` set time=from_unixtime(
    # unix_timestamp('2019-12-05')
    # + floor(
    #     rand() * ( unix_timestamp('2019-12-05') - unix_timestamp('2019-11-05') + 1 )
    # )
    # )

    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()
    test_pig_price_latest_date()
    session.commit()
    session.close()
    # create_bg_tables(BIG_DATA_DATABASE)

    # create_pigs_live_table()

    # count_pigs_deed_map()







