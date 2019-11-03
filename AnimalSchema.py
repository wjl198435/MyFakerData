from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy import Column, String, Integer, Text, ForeignKey, Table, DateTime, FLOAT
import random
from faker import Faker
faker = Faker(locale='zh_CN')

from config import DB_URL

database = 'iot_db'
engine = create_engine(DB_URL.format(database))
Base = declarative_base()



class User(Base):

    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    username = Column(String(64), nullable=False, index=True)
    password = Column(String(64), nullable=False)

    role_id = Column(Integer, ForeignKey('roles.id'))
    role = relationship('Role', backref='role')

    company_id = Column(Integer, ForeignKey('companies.id'))
    company = relationship('Company', backref='company')

    # company = relationship('Company', secondary='user_company', backref='companies')
    # company_id = Column(Integer, ForeignKey('companies.id'))
    # company = relationship('Company', backref='company')
    # company = relationship('Company', backref='company')
    # roles = relationship('Role', secondary='user_role', backref='users')



    def __repr__(self):
        return '%s(%r)' % (self.__class__.__name__, self.username)


class UserInfo(Base):

    __tablename__ = 'userinfos'

    id = Column(Integer, primary_key=True)
    email = Column(String(64), nullable=False, index=True)
    friendly_name = Column(String(64))
    qq = Column(String(11))
    phone = Column(String(11))
    link = Column(String(64))
    join_datetime = Column(DateTime,nullable=False)
    roles = Column(String(11))

    lat = Column(FLOAT)
    lon = Column(FLOAT)
    # company = Column(Integer, ForeignKey('companies.id'))

    user_id = Column(Integer, ForeignKey('users.id'))
    userinfo = relationship('User', backref='userinfo', uselist=False)


user_role = Table(
    'user_role', Base.metadata,
    Column('user_id', Integer, ForeignKey('users.id')),
    Column('role_id', Integer, ForeignKey('roles.id'))
)

Roles = ["法人","总经理","经理","主管","组长","工人"]
class Role(Base):

    __tablename__ = 'roles'

    id = Column(Integer, primary_key=True)
    name = Column(String(10), nullable=False, index=True)
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
    name = Column(String(64))  # 公司名
    address = Column(String(64))  # 地址
    contact = Column(String(11))  # 联系电话
    scopes_id = Column(Integer, ForeignKey('companies.id'))
    scopes = relationship('Scope', secondary='company_scope', backref='companies')


    # scope = relationship('Scope', secondary='company_scope', backref='scopes')
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

    id = Column(Integer, primary_key=True)
    name = Column(String(10), nullable=False, index=True)
    def __repr__(self):
        return '%s(%r)' % (self.__class__.__name__, self.name)


class Species(Base):

    __tablename__ = 'species'

    id = Column(Integer, primary_key=True)
    name = Column(String(64), nullable=False, index=True)
    #
    # sn = Column(String(18), nullable=False, index=True)  # 身份序列号
    # birthday = Column(DateTime, nullable=False)
    # join_date = Column(DateTime, nullable=False)
    # friendly_name = Column(String(64))
    # sex = Column(String(2))
    # weight = Column(FLOAT)
    # temperature = Column(FLOAT)


class Category(Base):

    __tablename__ = 'categories'

    id = Column(Integer, primary_key=True)
    name = Column(String(64), nullable=False, index=True)
    # animals = relationship('Animal', backref='category')

    def __repr__(self):
        return '%s(%r)' % (self.__class__.__name__, self.name)


if __name__ == '__main__':
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()
    sum = 10

    faker_scopes= [Scope(name=CategoryName[i]) for i in range(len(CategoryName))]

    faker_cats= [Category(name=CategoryName[i]) for i in range(len(CategoryName))]

    companies = [Company(
        corporate =faker.name(),
        name=faker.company(),

    ) for i in range(sum)]

    for i in range(sum):
        for scope in random.sample(faker_scopes, random.randint(1, 2)):
            companies[i].scopes.append(scope)

    session.add_all(companies)

    users = [User(
        username=faker.name(),
        password=faker.random_number(digits=random.randint(4, 10)),
    ) for i in range(sum)]

    userinfos = [UserInfo(
        friendly_name=faker.name(),
        email = faker.ascii_company_email(),
        phone=faker.phone_number(),
        lat = faker.latitude(),
        lon = faker.longitude(),
        join_datetime=faker.past_datetime(),
    ) for i in range(sum)]


    faker_roles= [Role(name=Roles[i]) for i in range(len(Roles))]

    for i in range(sum):
        users[i].userinfo.append(userinfos[i])
        users[i].role = random.choice(faker_roles)
        users[i].company = random.choice(companies)

    session.add_all(users)

    # animal = Species(name = Column(String(18), nullable=False, index=True)
    #                 # name="ww",
    #                 # birthday = faker.past_datetime(),
    #                 # join_date = faker.past_datetime(),
    #                 # category=random.choice(faker_cats)
    #                 )
    # session.add(animal)
    ## 生成动物数据
    # for i in range(10*sum):
    #     animal = Animal(
    #                     sn = Column(String(18), nullable=False, index=True)
    #                     # name="ww",
    #                     # birthday = faker.past_datetime(),
    #                     # join_date = faker.past_datetime(),
    #                     # category=random.choice(faker_cats)
    #                     )
    #     session.add(animal)


    session.commit()