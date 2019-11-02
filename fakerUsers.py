# coding: utf-8
from faker import Faker
import json
import random
from IOTSchema import User, UserInfo
from IOTSchema import Company
from IOTSchema import Roles,Role
from IOTSchema import engine
from sqlalchemy.orm import sessionmaker

faker = Faker(locale='zh_CN')
female = ['男','女']

def fakerUser(num=10):
    faker_users = [User(
        username=faker.user_name(),
        password=faker.md5(),
        tel=faker.phone_number(),
        email=faker.email(),
        join_datetime=faker.past_datetime(),
    ) for i in range(num)]
    return faker_users

def fakerUserInfo(num=10):
    _num = int(num)
    UserInfos = [UserInfo(
        friendly_name = faker.name(),
        sex = random.choice(female),
        id_card = faker.credit_card_number(),
        qq = faker.random_number(digits=random.randint(4, 10)),
        address = faker.street_address(),
        lat = faker.latitude(),
        lon = faker.longitude(),
        scale = faker.random_number(digits=random.randint(2,5))*100,
        total_scale =  faker.random_number(digits=random.randint(4,5))*100,
        social_credit_issue = faker.credit_card_number(),
        credit_rate = faker.random_digit(),
        link = faker.url(),
        license_id = faker.random_number(10),
        province = faker.province(),
        company = faker.company(),
        # user_id = random.choice(users)
    ) for i in range(_num)]
    return UserInfos

#
# class User(Base):
#
#     __tablename__ = 'users'
#
#     id = Column(Integer, primary_key=True)
#     username = Column(String(64), nullable=False, index=True)
#     password = Column(String(64), nullable=False)
#     email = Column(String(64), nullable=False, index=True)
#
#
#     def __repr__(self):
#         return '%s(%r)' % (self.__class__.__name__, self.username)
#
# sensor_type = ("temp", "humi", "light", "aqi")
# sensor_unit_list = ('℃', 'rh%', 'lum', 'ug')
# sensor_range_min = (-50, 0, 0, 0)
# sensor_range_max = (50, 100, 10000, 5000)
#
# def fake_sensor_data(clientid,user_name,sensor_type='temp',unit='℃',min=0,max=100):
#     temp = {
#         'username': user_name,
#         'clientid': clientid,
#         'company': f.company_prefix(),
#         'type': sensor_type,
#         'value': f.random_int(min=min, max=max),
#         'uptime': f.unix_time(),
#         'unit': unit,
#         'mac': f.mac_address(),
#         'isbn': f.isbn10(), #设备编号
#         "geo": {
#             "key": "zh_CN",
#             "latitude": float(f.latitude()),
#             "longitude": float(f.longitude()),
#             "name": "中国",
#         },
#     }
#
#     json_str = json.dumps(temp)
#     return json_str
#




if __name__ == '__main__':
    # users = fakerUser(10)
    Session = sessionmaker(bind=engine)
    session = Session()

    number = 10


    faker_users = [User(
        # username=faker.user_name(),
        # password=faker.md5(),
        # tel=faker.phone_number(),
        # email=faker.email(),
        # join_datetime=faker.past_datetime(),
    ) for i in range(number)]

    session.add_all(faker_users)

    faker_Roles = [Role(name=Roles[i]) for i in range(len(Roles))]

    session.add_all(faker_Roles)

    for i in range(10):
        usesinfo = UserInfo(
                # friendly_name = faker.name(),
                # sex = random.choice(female),
                # id_card = faker.credit_card_number(),
                # qq = faker.random_number(digits=random.randint(4, 10)),
                # address = faker.street_address(),
                # lat = faker.latitude(),
                # lon = faker.longitude(),
                # province = faker.province(),
                # scale = faker.random_number(digits=random.randint(2,5))*100,
                # total_scale =  faker.random_number(digits=random.randint(4,5))*100,
                # social_credit_issue = faker.credit_card_number(),
                # credit_rate = faker.random_digit(),
                # link = faker.url(),
                # license_id = faker.random_number(10),

                # company = faker.company(),
                user_id = random.choice(faker_users),
            )

        # for role in random.sample(faker_Roles, random.randint(1, 2)):
        #     usesinfo.roles.append(role)

        session.add(usesinfo)
    #
    #     print(usesinfo)


    session.commit()