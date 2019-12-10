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



## ui-lovelace.yaml
    ```
          - cards:
              - aspect_ratio: 60%
                columns: 3
                entity: climate.house1_room1
                name: room1
                theme: 明亮蓝
                type: thermostat
              - entities:
                  - entity: sensor.house1_room1_temperature
                    name: 温度
                  - entity: sensor.house1_room1_humidity
                    name: 湿度
                  - entity: sensor.house1_room1_pm25
                    name: PM2.5
                  - entity: sensor.house1_room1_illuminance
                    name: 亮度
                  - entity: sensor.house1_room1_nh3
                    name: 氨气
                theme: 黑-蓝
                type: glance
            type: vertical-stack

    ```
    
    
    ```
    - entities:
      - entity: sensor.house1_room2_humidity
        name: 温度
      - entity: sensor.house1_room2_illuminance
        name: 亮度
      - entity: sensor.house1_room2_nh3
        name: 氨气
      - entity: sensor.house1_room2_temperature
        name: 温度
      - entity: sensor.house1_room2_pm25
        name: pm2.5
      - entity: climate.house1_room1
        name: 空调
      - entity: fan.house1_room1
        name: 风扇
      - entity: light.house1_room1
        name: 灯光
      - entity: switch.house1_room1_cool    
        name: 制冷开关
      - entity: switch.house1_room1_heater 
        name: 加热开关   
      - entity: switch.house1_room1_switch
        name: 开关 
      - show_header_toggle: false
    theme: 灰-绿
    title: room1
    type: entities
    ```