import datetime
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy import Column, String, Integer, Text, ForeignKey, Table, DateTime, FLOAT, Text
import random
from faker import Faker
faker = Faker(locale='zh_CN')

from config import DB_URL

database = 'iot_db'
engine = create_engine(DB_URL.format(database))
Base = declarative_base()

class User(Base):

    __tablename__ = 'users'

    id = Column(Integer, primary_key=True,index=True)
    username = Column(String(64), nullable=False, index=True)
    password = Column(String(64), nullable=False)

    role_id = Column(Integer, ForeignKey('roles.id'))
    role = relationship('Role', backref='role')

    company_id = Column(Integer, ForeignKey('companies.id'))
    company = relationship('Company', backref='company')


    userinfo_id = Column(Integer, ForeignKey('userinfos.id'))
    userinfo = relationship('UserInfo', backref='userinfo', uselist=False)

    # company = relationship('Company', secondary='user_company', backref='companies')
    # company_id = Column(Integer, ForeignKey('companies.id'))
    # company = relationship('Company', backref='company')
    # company = relationship('Company', backref='company')
    # roles = relationship('Role', secondary='user_role', backref='users')



    def __repr__(self):
        return '%s(%r)' % (self.__class__.__name__, self.username)


class UserInfo(Base):

    __tablename__ = 'userinfos'

    id = Column(Integer, primary_key=True,index=True)
    email = Column(String(64), nullable=False, index=True)
    friendly_name = Column(String(64))
    qq = Column(String(11))
    phone = Column(String(11))
    # link = Column(String(64))
    join_datetime = Column(DateTime,nullable=False)
    # roles = Column(String(11))

    lat = Column(FLOAT)
    lon = Column(FLOAT)
    # company = Column(Integer, ForeignKey('companies.id'))

    # user_id = Column(Integer, ForeignKey('users.id'))
    # userinfo = relationship('User', backref='userinfo', uselist=False)




# user_role = Table(
#     'user_role', Base.metadata,
#     Column('user_id', Integer, ForeignKey('users.id')),
#     Column('role_id', Integer, ForeignKey('roles.id'))
# )

Roles = ["法人","总经理","经理","主管","组长","工人"]
class Role(Base):

    __tablename__ = 'roles'

    id = Column(Integer, primary_key=True,index=True)
    name = Column(String(10), nullable=False, index=True,unique=True)
    friendly_name = Column(String(10))


    def __repr__(self):
        return '%s(%r,%s)' % (self.__class__.__name__, self.name,self.friendly_name)


# user_company = Table(
#     'user_company', Base.metadata,
#     Column('user_id', Integer, ForeignKey('users.id')),
#     Column('company_id', Integer, ForeignKey('companies.id'))
# )


class Company(Base):

    __tablename__ = 'companies'

    id = Column(Integer, primary_key=True,index=True)
    name = Column(String(64))  # 公司名
    corporate =  Column(String(64),nullable=False, index=True)  # 法人

    scale = Column(Integer)  # 养殖现规模
    total_scale = Column(Integer)  # 总规模
    social_credit_issue = Column(String(18))  # 企业社会信用
    credit_rate = Column(Integer)  # 信用评级

    lat = Column(FLOAT)  # 经纬度
    lon = Column(FLOAT)  # 经纬度
    link = Column(String(64))  # 网站链接
    license_id = Column(Integer)   # 获取授权商品id起始编号
    province = Column(String(10))
    city = Column(String(16))  # 所在城市
    street_address =  Column(String(50))  # 街道

    # address = Column(String(64))  # 地址
    contact = Column(String(11))  # 联系电话
    # scopes_id = Column(Integer, ForeignKey('companies.id'))
    scopes = relationship('Scope', secondary='company_scope', backref='companies')
    animals = relationship('Animal', backref='producer')   # 拥有产品
    # scope = relationship('Scope', secondary='company_scope', backref='scopes')  # 营业范围
    # work = relationship('User', backref='work')

    def __repr__(self):
        return '%s(%r,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)' \
               % (self.__class__.__name__, self.corporate,self.scale,self.total_scale,self.social_credit_issue,self.credit_rate,
                  self.lat,self.lon,self.link,self.license_id,self.province,self.city,self.street_address,self.company,self.address,self.contact)


company_scope = Table('company_scope', Base.metadata,
                      Column('company_id', Integer, ForeignKey('companies.id')),
                      Column('scope_id', Integer, ForeignKey('scopes.id'))
                     )

## 营业范围
CategoryName = ['母猪','种猪','育肥猪','猪苗']

class Scope(Base):

    __tablename__ = 'scopes'

    id = Column(Integer, primary_key=True,index=True)
    name = Column(String(10), nullable=False, index=True,unique=True)
    def __repr__(self):
        return '%s(%r)' % (self.__class__.__name__, self.name)


animal_keeper = Table(
    'animal_keeper', Base.metadata,
    Column('user_id', Integer, ForeignKey('users.id')),
    Column('animal_id', Integer, ForeignKey('animals.id'))
)



class Animal(Base):

    __tablename__ = 'animals'

    id = Column(Integer, primary_key=True,index=True)
    # name = Column(String(64), nullable=False, index=True)
    friendly_name = Column(String(64))
    sn = Column(String(18), nullable=False, index=True)  # 身份序列号
    birthday = Column(DateTime, nullable=False)
    join_date = Column(DateTime, nullable=False)
    friendly_name = Column(String(64))
    sex = Column(String(2))
    weight = Column(FLOAT)
    temperature = Column(FLOAT)

    cate_id = Column(Integer, ForeignKey('categories.id'))
    company_id = Column(Integer, ForeignKey('companies.id'))

    camera_id = Column(Integer, ForeignKey('cameras.id'))
    camera = relationship('Camera', backref='camera')

    keepers = relationship('User', secondary='animal_keeper', backref='keepers')

    animalinfo_id = Column(Integer, ForeignKey('animalinfos.id'))
    animalinfo = relationship('AnimalInfo', backref='animalinfo', uselist=False)

Animal_Sex = ["公","母"]
Sick_times = [0,0,0,0,0,0,0,0,0,0,0,1,1,1,2,2,3,4,5,6,7]
Sick_days = [1,1,1,1,2,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16]

health_stats = ['健康','受伤','咳嗽','皮肤过敏','发烧','生病','死亡']
health_stats_index = [0,0,0,0,0,0,0,0,0,0,0,1,2,3,4,5,5,6]

action_status = ['进食','睡眠','运动','打斗']  # 行为状态
action_status_index = [0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,1,1,1,2,2,2,2,3]
class AnimalInfo(Base):

    __tablename__ = 'animalinfos'

    id = Column(Integer, primary_key=True,index=True)

    address = Column(String(64))  # 所属单元(那栋楼、那单元)
    sick_times = Column(Integer)  # 生病次数
    total_sick_days = Column(Integer)  # 生病总天数

    total_meters = Column(Integer)  # 运动总米数
    day_meters = Column(Integer)  # 当天运动米数
    vaccine_times = Column(Integer)  # 注射疫苗次数
    total_feed_weight = Column(FLOAT)  # 总消耗饲料量
    total_feed_times = Column(Integer)   # 总进食次数
    total_feed_seconds = Column(Integer)  # 总进食时长
    day_feed_weight = Column(FLOAT)  # 当天进食总量
    day_feed_times = Column(Integer)  # 当天进食次数
    day_feed_seconds = Column(Integer)  # 当天进食时长
    day_cough_times = Column(Integer)  # 当天咳嗽、喷嚏次数

    lat = Column(FLOAT)  # 经纬度
    lon = Column(FLOAT)  # 经纬度

    health_rate = Column(Integer)  # 健康等级
    health_status = Column(String(6)) # 健康状态
    action_status = Column(String(6))  #当前行为状态




    # camera = Column(Integer, ForeignKey('cameras.id'))  # 监控摄像头设备号
    # current_state = Column(Integer, ForeignKey('states.id'))  # 进食、睡眠、运动，打斗
    # health_state = Column(Integer, ForeignKey('healthes.id'))  # 健康状态


class Category(Base):

    __tablename__ = 'categories'

    id = Column(Integer, primary_key=True,index=True)
    name = Column(String(64), nullable=False, index=True)
    animals = relationship('Animal', backref='category')

    def __repr__(self):
        return '%s(%r)' % (self.__class__.__name__, self.name)

domain =['temperature','humidity','luminance','aqi','fans','NH3','switch']
domain_friendly_name = ['温度','湿度','亮度','空气质量','风速','氨气','开关']
unit =['℃','RH%','lu','pm2.5','m/s','g/L' ,'']

class Sensor(Base):
    __tablename__ = 'sensors'

    id = Column(Integer, primary_key=True,index=True)
    sn = Column(String(20),nullable=False, index=True)   # 设备序列号
    friendly_name = Column(String(64))  # 设备名称

    event_id = Column(Integer)  # 事件id
    entity_id = Column(Integer)  # 运行实例id

    model = Column(String(20))  # 产品型号
    mac = Column(String(17))  # mac 地址
    loc = Column(String(64))  # 安装位置
    domain = Column(String(10))  # 设备类型
    unit = Column(String(10)) # 设备单位
    state = Column(String(10))  # 当前状态
    attributes = Column(Text)  # 当前属性

    last_changed = Column(DateTime)  #最后改变时间
    last_updated = Column(DateTime)  #最后更新时间
    created = Column(DateTime)     # 创建时间

    sensorinfo_id = Column(Integer, ForeignKey('sensorinfos.id'))
    sensorinfo = relationship('SensorInfo', backref='sensorinfo', uselist=False)



class SensorInfo(Base):

    __tablename__ = 'sensorinfos'

    id = Column(Integer, primary_key=True,index=True)

    lat = Column(FLOAT)  # 经纬度
    lon = Column(FLOAT)  # 经纬度
    address = Column(String(64))

    power = Column(FLOAT)  # 功耗
    manufacturers = Column(String(18))   # 设备提供商
    manufactures_tel = Column(String(11))  # 设备提供商联系电话

    def __repr__(self):
        return '%s(%r)' % (self.__class__.__name__, self.name)


class Camera(Base):
    __tablename__ = 'cameras'

    id = Column(Integer, primary_key=True,index=True)
    sn = Column(String(20),nullable=False, index=True)   # 设备序列号
    friendly_name = Column(String(64))  # 设备名称

    event_id = Column(Integer)  # 事件id
    entity_id = Column(Integer)  # 运行实例id

    model = Column(String(20))  # 产品型号
    mac = Column(String(17))  # mac 地址
    loc = Column(String(64))  # 安装位置
    domain = Column(String(10))  # 设备类型
    unit = Column(String(10)) # 设备单位
    state = Column(String(10))  # 当前状态
    attributes = Column(Text)  # 当前属性

    last_changed = Column(DateTime)  #最后改变时间
    last_updated = Column(DateTime)  #最后更新时间
    created = Column(DateTime)     # 创建时间

    camerainfo_id = Column(Integer, ForeignKey('camerainfos.id'))
    camerainfo = relationship('CameraInfo', backref='camerainfo', uselist=False)



class CameraInfo(Base):

    __tablename__ = 'camerainfos'

    id = Column(Integer, primary_key=True,index=True)

    lat = Column(FLOAT)  # 经纬度
    lon = Column(FLOAT)  # 经纬度
    address = Column(String(64))

    power = Column(FLOAT)  # 功耗
    manufacturers = Column(String(18))   # 设备提供商
    manufactures_tel = Column(String(11))  # 设备提供商联系电话

    def __repr__(self):
        return '%s(%r)' % (self.__class__.__name__, self.name)


if __name__ == '__main__':
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()
    sum_company = 10
    sum_user = sum_company*10
    sum_animal = sum_user*5

    sum_sensors = 100
    sum_cameras =300

    try:
        faker_scopes= [Scope(name=CategoryName[i]) for i in range(len(CategoryName))]
        faker_cats= [Category(name=CategoryName[i]) for i in range(len(CategoryName))]  # 主营物种范围
        faker_roles= [Role(name=Roles[i]) for i in range(len(Roles))]   # 创建用户角色
    except :
        pass

    companies = [Company(       # 构建公司信息
        corporate =faker.name(),
        name=faker.company(),
        scale =random.randint(100,1000)*100,  # 当前养殖现规模
        total_scale =random.randint(100,1000)*200,  # 总养殖现规模
        social_credit_issue = faker.isbn13(),
        credit_rate = random.randint(0,10),

        lat=faker.latitude(),
        lon=faker.longitude(),

        link = faker.url() , # 企业网站
        license_id = random.randint(1,10000000)*100,
        province = faker.province(),
        city = faker.district(),
        street_address = faker.street_address(),
        contact = faker.phone_number(),
        # scopes = [random.sample(faker_scopes, random.randint(1, 2))]
    ) for i in range(sum_company)]

    for i in range(sum_company):      # 添加企业 营业范围
        for scope in random.sample(faker_scopes, random.randint(1, 2)):
            companies[i].scopes.append(scope)

    session.add_all(companies)

    users = [User(      #构建用户信息
        username=faker.user_name(),
        password=faker.random_number(digits=random.randint(4, 10)),
    ) for i in range(sum_user)]

    userinfos = [UserInfo(   # 构建用户详情
        friendly_name=faker.name(),
        email = faker.ascii_company_email(),
        phone=faker.phone_number(),
        qq = faker.random_number(digits=random.randint(4, 10)),
        lat = faker.latitude(),
        lon = faker.longitude(),
        join_datetime=faker.past_datetime(),
    ) for i in range(sum_user)]

    for i in range(sum_user):     # 为用户添加角色
        # users[i].userinfo.append(userinfos[i])
        users[i].userinfo = userinfos[i]
        users[i].role = random.choice(faker_roles)
        users[i].company = random.choice(companies)

    session.add_all(users)


    # 摄像头
    cameras = [
        Camera(
            sn = faker.isbn10(),
            model = faker.word(),
            loc = faker.street_name(),
        )
        for i in range(sum_cameras) ]

    camerainfos = [
        CameraInfo(
            address = faker.street_address()
        )
        for i in range(sum_cameras) ]

    session.add_all(cameras)

    for i in range(sum_cameras):
        cameras[i].camerainfo = camerainfos[i]


    animalinfos = [AnimalInfo(
        address=faker.street_address(),
        lat=faker.latitude(),
        lon=faker.longitude(),
        sick_times = random.choice(Sick_times), # 生病次数
        total_sick_days = random.choice(Sick_days),  # 生病总天数
        total_meters = random.randint(1000000,10000000), # 运动总米数
        day_meters = random.randint(1000,20000),  # 当天运动米数
        vaccine_times = random.randint(2,5), # 注射疫苗次数
        total_feed_weight = random.uniform(60000.0,1000000.0),  # 总消耗饲料量
        total_feed_times = random.randint(10,2000),   # 总进食次数
        total_feed_seconds = random.randint(14400000,28800000),  # 总进食时长
        day_feed_weight = random.uniform(0.0,5000.0),  # 当天进食总量
        day_feed_times = random.randint(0,8),  # 当天进食次数
        day_feed_seconds = random.randint(0,7200),  # 当天进食时长
        day_cough_times = random.randint(0,100), # 当天咳嗽、喷嚏次数
        health_rate = random.randint(0,10),
        health_status = health_stats[random.choice(health_stats_index)],
        action_status = action_status[random.choice(action_status_index)]

    ) for i in range(sum_animal)]

    for i in range(sum_animal):
        animal = Animal(
                friendly_name = faker.user_name(),
                sn = faker.random_number(10),
                birthday = faker.past_datetime()-datetime.timedelta(days=faker.random_int(min=30,max=180)),
                category=random.choice(faker_cats),
                producer = random.choice(companies),
                sex = random.choice(Animal_Sex),
                weight = random.uniform(30.0,450.0),
                temperature = random.uniform(36.5,40.0),
                camera = random.choice(cameras),

        )

        # animal.animalinfo.append(animalinfos[i])
        animal.animalinfo = animalinfos[i]

        for keeper in random.sample(users, random.randint(1, 3)):
            animal.keepers.append(keeper)
        delta = datetime.timedelta(days=faker.random_int(min=30,max=60))
        join_date = animal.birthday+delta
        animal.join_date = join_date
        # print(animal.birthday,":",join_date)
        session.add(animal)


    # model = Column(String(20))  # 产品型号
    # mac = Column(String(17))  # mac 地址
    # loc = Column(String(64))  # 安装位置
    # domain = Column(String(10))  # 设备类型
    # unit = Column(String(10)) # 设备单位
    # state = Column(String(10))  # 当前状态
    # attributes = Column(Text)  # 当前属性
    #
    # last_changed = Column(DateTime)  #最后改变时间
    # last_updated = Column(DateTime)  #最后更新时间
    # created = Column(DateTime)     # 创建时间


    sensors = [
        Sensor(
            sn = faker.isbn10(),
            model = faker.word(),
            loc = faker.street_name(),
        )
        for i in range(sum_sensors) ]

    sensorinfos = [
        SensorInfo(
            address = faker.street_address()
        )
        for i in range(sum_sensors) ]

    for i in range(sum_sensors):
        sensors[i].sensorinfo = sensorinfos[i]
    session.add_all(sensors)
    # session.add_all(sensorinfos)

    session.commit()
