### 参考教程 influx-mqqt  https://segmentfault.com/a/1190000012514865
### sqlalchemy https://www.cnblogs.com/mrchige/p/6389588.html
    https://www.cnblogs.com/goldsunshine/p/9269880.html
### Faker 源码 https://github.com/joke2k/faker

### https://www.runoob.com/python3/python-mysql-connector.html
## 环境准备
 ```
 conda activate homeassistant
 pip install Faker
 sudo pip install sqlalchemy
 pip install pymysql
 python3 FakeSensor.py

 conda acitvate homeassistant
 conda install -n homeassistant paho-mqtt

 pip install mysql-connector
```
## influx

## tables （ one to on）
```$xslt
class Sensor(Base):
    __tablename__ = 'sensors'
    id = Column(Integer, primary_key=True)

    sensorinfo_id = Column(Integer, ForeignKey('sensorinfos.id'))
    sensorinfo = relationship('SensorInfo', backref='sensorinfo', uselist=False)
    
class SensorInfo(Base):

    __tablename__ = 'sensorinfos'
    id = Column(Integer, primary_key=True)    


for i in range(sum_sensors):
        sensors[i].sensorinfo = sensorinfos[i]


```

## 基于conda faker sqlalchemy 生产模拟数据，并基于mqtt 进行发送


## mysql 导出数据库表结构:
```
mysqldump -hlocalhost -uroot -proot -d iot_db2  > iot_db2.sql
```

select
$__timeGroupAlias(time,$__interval) ,
count(animals.id)
from animals 
join animalinfos on `animals`.`animalinfo_id`= animalinfos.id 
where company_id=${company_id} and health_status <> '死亡' and $__timeFilter(animalinfos.time)