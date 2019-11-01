from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy import Column, String, Integer, Text, ForeignKey, Table, DateTime, FLOAT
from config import DB_URL

database = 'IOT'
engine = create_engine(DB_URL.format(database))
Base = declarative_base()

class User(Base):

    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    username = Column(String(64), nullable=False, index=True)
    password = Column(String(64), nullable=False)
    tel = Column(String(11), nullable=False, index=True)
    email = Column(String(64), nullable=False, index=True)
    join_datetime = Column(DateTime,nullable=False)
    # articles = relationship('Article', backref='author')

    userinfo = relationship('UserInfo', backref='user', uselist=False)
    roles = relationship('Role', secondary='user_role', backref='user')

    company = Column(Integer, ForeignKey('companies.id'))
    # userrole = relationship('Role', backref='role')

    def __repr__(self):
        return '%s(%r,%s,%s,%s,%s)' % (self.__class__.__name__, self.username,self.password,self.tel,self.email,self.join_datetime)



class UserInfo(Base):

    __tablename__ = 'userinfos'

    id = Column(Integer, primary_key=True)
    friendly_name = Column(String(64),nullable=False, index=True)
    sex = Column(String(2))  # 性别
    id_card = Column(String(18))  # 身份证号
    qq = Column(String(11))
    address = Column(String(64))  # 地址
    lat = Column(FLOAT)  # 经纬度
    lon = Column(FLOAT)  # 经纬度
    province = Column(String(10))
    # role = Column(Integer, ForeignKey('roles.id'))  # 角色
    # cate_id = Column(Integer, ForeignKey('categories.id')) ## 主营类别
    user_id = Column(Integer, ForeignKey('users.id'))



    def __repr__(self):
        return '%s(%r,%s,%s,%s,%s,%s,%s,%s,%s)' \
               % (self.__class__.__name__, self.friendly_name,self.sex,self.id_card,self.qq,self.province,
                  self.address,self.lat,self.lon,self.user_id)

user_role = Table(
    'user_role', Base.metadata,
    Column('users_id', Integer, ForeignKey('users.id')),
    Column('role_id', Integer, ForeignKey('roles.id'))
)

## 用户角色
class Role(Base):

    __tablename__ = 'roles'

    id = Column(Integer, primary_key=True)
    name = Column(String(10), nullable=False, index=True)
    def __repr__(self):
        return '%s(%r)' % (self.__class__.__name__, self.name)





class Company(Base):

    __tablename__ = 'companies'

    id = Column(Integer, primary_key=True)
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
    company = Column(String(64))  # 公司名
    address = Column(String(64))  # 地址
    contact = Column(String(11))  # 联系电话
    scope = relationship('Scope', secondary='company_scope', backref='scopes')
    work = relationship('User', backref='work')

    def __repr__(self):
        return '%s(%r,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)' \
               % (self.__class__.__name__, self.corporate,self.scale,self.total_scale,self.social_credit_issue,self.credit_rate,
                  self.lat,self.lon,self.link,self.license_id,self.province,self.city,self.street_address,self.company,self.address,self.contact)


company_scope = Table(
    'company_scope', Base.metadata,
    Column('companies_id', Integer, ForeignKey('companies.id')),
    Column('scope_id', Integer, ForeignKey('scopes.id'))
)
## 营业范围
class Scope(Base):

    __tablename__ = 'scopes'

    id = Column(Integer, primary_key=True)
    name = Column(String(10), nullable=False, index=True)
    def __repr__(self):
        return '%s(%r)' % (self.__class__.__name__, self.name)

# class Poultry(Base):
#
#     __tablename__ = 'poultries'
#
#     id = Column(Integer, primary_key=True)
#     sn = Column(String(18), nullable=False, index=True)  # 身份序列号
#     friendly_name = Column(String(64))
#     sex = Column(String(2))
#     weight = Column(FLOAT)
#     temperature = Column(FLOAT)
#     join_datetime = Column(DateTime, nullable=False)
#     # title = Column(String(255), nullable=False, index=True)
#     # content = Column(Text)
#     user_id = Column(Integer, ForeignKey('users.id'))
#     cate_id = Column(Integer, ForeignKey('categories.id'))
#     tags = relationship('Tag', secondary='poultry_tag', backref='poultries')
#
#     def __repr__(self):
#         return '%s(%r)' % (self.__class__.__name__, self.title)

# class PoultryInfo(Base):
#
#     __tablename__ = 'poultryinfos'
#
#     id = Column(Integer, primary_key=True)
#     friendly_name = Column(String(64))
#     address = Column(String(64))  # 所属单元(那栋楼、那单元)
#     sick_times = Column(Integer)  # 生病次数
#     total_sick_days = Column(Integer)  # 生病总天数
#     health_state = Column(Integer, ForeignKey('healthes.id'))  # 健康状态
#     total_meters = Column(Integer)  # 运动总米数
#     day_meters = Column(Integer)  # 当天运动米数
#     vaccine_times = Column(Integer)  # 注射疫苗次数
#     total_feed_weight = Column(FLOAT)  # 总消耗饲料量
#     total_feed_times = Column(Integer)   # 总进食次数
#     total_feed_seconds = Column(Integer)  # 总进食时长
#     day_feed_weight = Column(FLOAT)  # 当天进食总量
#     day_feed_times = Column(Integer)  # 当天进食次数
#     day_feed_seconds = Column(Integer)  # 当天进食时长
#     day_cough_times = Column(Integer)  # 当天咳嗽、喷嚏次数
#
#     lat = Column(FLOAT)  # 经纬度
#     long = Column(FLOAT)  # 经纬度
#
#     health_rate = Column(Integer)  # 健康等级
#     keeper = Column(String(10))     # 管理饲养员
#     camera = Column(Integer, ForeignKey('cameras.id'))  # 监控摄像头设备号
#     current_state = Column(Integer, ForeignKey('states.id'))  # 进食、睡眠、运动，打斗
#
#
# class State(Base):
#     __tablename__ = 'states'
#
#     id = Column(Integer, primary_key=True)
#     state = Column(String(6), nullable=False, index=True)
#     friendly_name = Column(String(64))
#     poultryInfo = relationship('PoultryInfo', backref='state')
#     def __repr__(self):
#         return '%s(%r)' % (self.__class__.__name__, self.state)
#
# class Health(Base):
#
#     __tablename__ = 'healthes'
#
#     id = Column(Integer, primary_key=True)
#     health = Column(String(6), nullable=False)
#     friendly_name = Column(String(64))
#     poultryInfo = relationship('PoultryInfo', backref='health')
#
#     def __repr__(self):
#         return '%s(%r)' % (self.__class__.__name__, self.health)
#
#
#
#
# class Category(Base):
#
#     __tablename__ = 'categories'
#
#     id = Column(Integer, primary_key=True)
#     name = Column(String(64), nullable=False, index=True)
#     friendly_name = Column(String(64))
#     userinfo = relationship('UserInfo', backref='category')
#
#     # articles = relationship('Article', backref='category')
#
#     def __repr__(self):
#         return '%s(%r)' % (self.__class__.__name__, self.name)
#
#
# poultry_tag = Table(
#     'poultry_tag', Base.metadata,
#     Column('poultry_id', Integer, ForeignKey('poultries.id')),
#     Column('tag_id', Integer, ForeignKey('tags.id'))
# )
#
#
# class Tag(Base):
#
#     __tablename__ = 'tags'
#
#     id = Column(Integer, primary_key=True)
#     name = Column(String(64), nullable=False, index=True)
#     friendly_name = Column(String(64))
#     def __repr__(self):
#         return '%s(%r)' % (self.__class__.__name__, self.name)


# class Sensor(Base):
#
#     __tablename__ = 'sensors'
#     sn = Column(String(18), nullable=False, index=True)  # 序列号
#     friendly_name = Column(String(64))
#
#     model = Column(String(20))  # 产品型号
#     mac = Column(String(17))
#     id = Column(Integer, primary_key=True)
#     state = Column(FLOAT)
#     location = Column(String(20))  # 安装位置
#     jion_datetime = Column(DateTime)  # 安装日期
#     power = Column(FLOAT)  # 功耗
#     manufacturers = Column(String(18))
#     manufactures_tel = Column(String(11))
#     lat = Column(FLOAT)  # 经纬度
#     long = Column(FLOAT)  # 经纬度
#     sensorcategories = Column(Integer, ForeignKey('sensorcategories.id'))
#     def __repr__(self):
#         return '%s(%r)' % (self.__class__.__name__, self.model)

# class SensorClass(Base):
#
#     __tablename__ = 'sensorcategories'

# class SensorCategories(Base):
#
#     __tablename__ = 'sensorcategories'
#
#     id = Column(Integer, primary_key=True)
#     type = Column(String(10), nullable=False, index=True)
#     unit = Column(String(4))  # 计量单位
#     SensorCategories = relationship('SensorCategories', backref='sensor')
#
#     def __repr__(self):
#         return '%s(%r)' % (self.__class__.__name__, self.role)

# class Switch(Base):
#
#     __tablename__ = 'switches'
#
#     id = Column(Integer, primary_key=True)
#     sn = Column(String(18), nullable=False, index=True)  # 序列号
#     model = Column(String(20))  # 产品型号
#     friendly_name = Column(String(64))
#     mac = Column(String(17))
#     location = Column(String(20))  # 安装位置
#     state = Column(Integer)  #
#     power = Column(FLOAT)  # 功耗
#     manufacturers = Column(String(18))
#     manufactures_tel = Column(String(11))
#     lat = Column(FLOAT)  # 经纬度
#     long = Column(FLOAT)  # 经纬度
#     def __repr__(self):
#         return '%s(%r)' % (self.__class__.__name__, self.model)

# class SwitchCategory(Base):
#
#     __tablename__ = 'switchcategories'
#
#     id = Column(Integer, primary_key=True)
#     state = Column(String(64), nullable=False, index=True)
#     switchcategory= relationship('SwitchCategory', backref='switch')
#
#     def __repr__(self):
#         return '%s(%r)' % (self.__class__.__name__, self.role)

# class Camera(Base):
#
#     __tablename__ = 'cameras'
#     id = Column(Integer, primary_key=True)
#     model = Column(String(20))  # 产品型号
#     friendly_name = Column(String(64))
#     link = Column(String(256), nullable=False, index=True)  # 视频播放地址
#     location = Column(String(20))  # 安装位置
#     sn = Column(String(18), nullable=False, index=True)  # 序列号
#     state = Column(Integer)
#     poultries= relationship('Poultry', backref='detect_dev')  # 监控那些家禽
#     mac = Column(String(17))  # mac_address
#     link = Column(String(128))  #视频播放地址
#     power = Column(FLOAT)  # 功耗
#     lat = Column(FLOAT)  # 经纬度
#     long = Column(FLOAT)  # 经纬度
#     manufacturers = Column(String(18))
#     manufactures_tel = Column(String(11))
#     capacities = relationship('Tag', secondary='camera_capacity', backref='capacities')
#     def __repr__(self):
#         return '%s(%r)' % (self.__class__.__name__, self.model)


# class Capacity(Base):
#
#     __tablename__ = 'capacities'
#
#     id = Column(Integer, primary_key=True)
#     name = Column(String(64), nullable=False, index=True)
#     friendly_name = Column(String(64))
#
#     def __repr__(self):
#         return '%s(%r)' % (self.__class__.__name__, self.name)
#
#
# camera_capacity = Table(
#     'camera_capacity', Base.metadata,
#     Column('cameras_id', Integer, ForeignKey('cameras.id')),
#     Column('capacities_id', Integer, ForeignKey('capacities.id'))
# )

if __name__ == '__main__':
    Base.metadata.create_all(engine)

    Session = sessionmaker(bind=engine)
    session = Session()