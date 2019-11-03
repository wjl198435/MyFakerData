# https://www.520mwx.com/view/31743

from sqlalchemy import Column, String, Integer, JSON, func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine



DB_URL ='mysql+pymysql://hass:hass@192.168.8.102/{}?charset=utf8'

Base = declarative_base()


class UserJson(Base):
    __tablename__ = 'user_json'
    id = Column(Integer, primary_key=True)
    content = Column(JSON)

    def __init__(self, content=None):
        self.content = content




database = 'iot_db'
engine = create_engine(DB_URL.format(database))
# engine = create_engine('postgresql://test:newpass@localhost:5432/test')

from sqlalchemy.orm import sessionmaker

# Construct a sessionmaker object
session = sessionmaker()

# Bind the sessionmaker to engine
session.configure(bind=engine)

# Create all the tables in the database which are
# defined by Base's subclasses such as User
# Base.metadata.create_all(engine)

data = {
    "code": 0,
    "data": {
        "users": [
            {
                "Age": 33,
                "ID": 1,
                "Url": "http://blog.golang.org/crankshaw@20170502235840",
                "UserName": "Crankshaw@20170502235840"
            },
            {
                "Age": 31,
                "ID": 2,
                "Url": "https://jack.github.io",
                "UserName": "Jack"
            },
            {
                "Age": 22,
                "ID": 3,
                "Url": "http://blog.golang.org/cock",
                "UserName": "Cock"
            },
            {
                "Age": 22,
                "ID": 4,
                "Url": "http://blog.golang.org/cock",
                "UserName": "Cock"
            },
            {
                "Age": 22,
                "ID": 5,
                "Url": "http://blog.golang.org/cock",
                "UserName": "Cock"
            },
            {
                "Age": 21,
                "ID": 6,
                "Url": "http://blog.golang.org/hickinbottom",
                "UserName": "Hickinbottom"
            },
            {
                "Age": 22,
                "ID": 7,
                "Url": "http://blog.golang.org/willy",
                "UserName": "Willy"
            },
            {
                "Age": 25,
                "ID": 8,
                "Url": "http://blog.golang.org/nutter",
                "UserName": "Nutter"
            },
            {
                "Age": 33,
                "ID": 9,
                "Url": "http://blog.golang.org/Pigg",
                "UserName": "Pigg"
            },
            {
                "Age": 22,
                "ID": 12,
                "Url": "http://blog.golang.org/cock",
                "UserName": "Cock"
            },
            {
                "Age": 22,
                "ID": 13,
                "Url": "http://blog.golang.org/cock",
                "UserName": "Cock"
            },
            {
                "Age": 21,
                "ID": 14,
                "Url": "http://blog.golang.org/hickinbottom",
                "UserName": "Hickinbottom"
            },
            {
                "Age": 22,
                "ID": 15,
                "Url": "http://blog.golang.org/willy",
                "UserName": "Willy"
            },
            {
                "Age": 25,
                "ID": 16,
                "Url": "http://blog.golang.org/nutter",
                "UserName": "Nutter"
            },
            {
                "Age": 33,
                "ID": 17,
                "Url": "http://blog.golang.org/Pigg",
                "UserName": "Pigg"
            },
            {
                "Age": 22,
                "ID": 20,
                "Url": "http://blog.golang.org/cock",
                "UserName": "Cock"
            },
            {
                "Age": 22,
                "ID": 21,
                "Url": "http://blog.golang.org/cock",
                "UserName": "Cock"
            },
            {
                "Age": 21,
                "ID": 22,
                "Url": "http://blog.golang.org/hickinbottom",
                "UserName": "Hickinbottom"
            },
            {
                "Age": 22,
                "ID": 23,
                "Url": "http://blog.golang.org/willy",
                "UserName": "Willy"
            },
            {
                "Age": 25,
                "ID": 24,
                "Url": "http://blog.golang.org/nutter",
                "UserName": "Nutter"
            },
            {
                "Age": 33,
                "ID": 25,
                "Url": "http://blog.golang.org/Pigg",
                "UserName": "Pigg"
            },
            {
                "Age": 22,
                "ID": 28,
                "Url": "http://blog.golang.org/cock",
                "UserName": "Cock"
            },
            {
                "Age": 22,
                "ID": 29,
                "Url": "http://blog.golang.org/cock",
                "UserName": "Cock"
            },
            {
                "Age": 21,
                "ID": 30,
                "Url": "http://blog.golang.org/hickinbottom",
                "UserName": "Hickinbottom"
            },
            {
                "Age": 22,
                "ID": 31,
                "Url": "http://blog.golang.org/willy",
                "UserName": "Willy"
            },
            {
                "Age": 25,
                "ID": 32,
                "Url": "http://blog.golang.org/nutter",
                "UserName": "Nutter"
            },
            {
                "Age": 33,
                "ID": 33,
                "Url": "http://blog.golang.org/Pigg",
                "UserName": "Pigg"
            },
            {
                "Age": 22,
                "ID": 36,
                "Url": "http://blog.golang.org/cock",
                "UserName": "Cock"
            },
            {
                "Age": 22,
                "ID": 37,
                "Url": "http://blog.golang.org/cock",
                "UserName": "Cock"
            },
            {
                "Age": 21,
                "ID": 38,
                "Url": "http://blog.golang.org/hickinbottom",
                "UserName": "Hickinbottom"
            },
            {
                "Age": 22,
                "ID": 39,
                "Url": "http://blog.golang.org/willy",
                "UserName": "Willy"
            },
            {
                "Age": 25,
                "ID": 40,
                "Url": "http://blog.golang.org/nutter",
                "UserName": "Nutter"
            },
            {
                "Age": 33,
                "ID": 41,
                "Url": "http://blog.golang.org/Pigg",
                "UserName": "Pigg"
            },
            {
                "Age": 22,
                "ID": 44,
                "Url": "http://blog.golang.org/cock",
                "UserName": "Cock"
            },
            {
                "Age": 22,
                "ID": 45,
                "Url": "http://blog.golang.org/cock",
                "UserName": "Cock"
            },
            {
                "Age": 21,
                "ID": 46,
                "Url": "http://blog.golang.org/hickinbottom",
                "UserName": "Hickinbottom"
            },
            {
                "Age": 22,
                "ID": 47,
                "Url": "http://blog.golang.org/willy",
                "UserName": "Willy"
            },
            {
                "Age": 25,
                "ID": 48,
                "Url": "http://blog.golang.org/nutter",
                "UserName": "Nutter"
            },
            {
                "Age": 33,
                "ID": 49,
                "Url": "http://blog.golang.org/Pigg",
                "UserName": "Pigg"
            },
            {
                "Age": 22,
                "ID": 52,
                "Url": "http://blog.golang.org/cock",
                "UserName": "Cock"
            },
            {
                "Age": 22,
                "ID": 53,
                "Url": "http://blog.golang.org/cock",
                "UserName": "Cock"
            },
            {
                "Age": 21,
                "ID": 54,
                "Url": "http://blog.golang.org/hickinbottom",
                "UserName": "Hickinbottom"
            },
            {
                "Age": 22,
                "ID": 55,
                "Url": "http://blog.golang.org/willy",
                "UserName": "Willy"
            },
            {
                "Age": 25,
                "ID": 56,
                "Url": "http://blog.golang.org/nutter",
                "UserName": "Nutter"
            },
            {
                "Age": 33,
                "ID": 57,
                "Url": "http://blog.golang.org/Pigg",
                "UserName": "Pigg"
            },
            {
                "Age": 22,
                "ID": 60,
                "Url": "http://blog.golang.org/cock",
                "UserName": "Cock"
            },
            {
                "Age": 22,
                "ID": 61,
                "Url": "http://blog.golang.org/cock",
                "UserName": "Cock"
            },
            {
                "Age": 21,
                "ID": 62,
                "Url": "http://blog.golang.org/hickinbottom",
                "UserName": "Hickinbottom"
            },
            {
                "Age": 22,
                "ID": 63,
                "Url": "http://blog.golang.org/willy",
                "UserName": "Willy"
            },
            {
                "Age": 25,
                "ID": 64,
                "Url": "http://blog.golang.org/nutter",
                "UserName": "Nutter"
            },
            {
                "Age": 33,
                "ID": 65,
                "Url": "http://blog.golang.org/Pigg",
                "UserName": "Pigg"
            },
            {
                "Age": 22,
                "ID": 68,
                "Url": "http://blog.golang.org/cock",
                "UserName": "Cock"
            },
            {
                "Age": 22,
                "ID": 69,
                "Url": "http://blog.golang.org/cock",
                "UserName": "Cock"
            },
            {
                "Age": 21,
                "ID": 70,
                "Url": "http://blog.golang.org/hickinbottom",
                "UserName": "Hickinbottom"
            },
            {
                "Age": 22,
                "ID": 71,
                "Url": "http://blog.golang.org/willy",
                "UserName": "Willy"
            },
            {
                "Age": 25,
                "ID": 72,
                "Url": "http://blog.golang.org/nutter",
                "UserName": "Nutter"
            },
            {
                "Age": 33,
                "ID": 73,
                "Url": "http://blog.golang.org/Pigg",
                "UserName": "Pigg"
            },
            {
                "Age": 22,
                "ID": 76,
                "Url": "http://blog.golang.org/cock",
                "UserName": "Cock"
            },
            {
                "Age": 22,
                "ID": 77,
                "Url": "http://blog.golang.org/cock",
                "UserName": "Cock"
            },
            {
                "Age": 21,
                "ID": 78,
                "Url": "http://blog.golang.org/hickinbottom",
                "UserName": "Hickinbottom"
            },
            {
                "Age": 22,
                "ID": 79,
                "Url": "http://blog.golang.org/willy",
                "UserName": "Willy"
            },
            {
                "Age": 25,
                "ID": 80,
                "Url": "http://blog.golang.org/nutter",
                "UserName": "Nutter"
            },
            {
                "Age": 33,
                "ID": 81,
                "Url": "http://blog.golang.org/Pigg",
                "UserName": "Pigg"
            },
            {
                "Age": 22,
                "ID": 84,
                "Url": "http://blog.golang.org/cock",
                "UserName": "Cock"
            },
            {
                "Age": 22,
                "ID": 85,
                "Url": "http://blog.golang.org/cock",
                "UserName": "Cock"
            },
            {
                "Age": 21,
                "ID": 86,
                "Url": "http://blog.golang.org/hickinbottom",
                "UserName": "Hickinbottom"
            },
            {
                "Age": 22,
                "ID": 87,
                "Url": "http://blog.golang.org/willy",
                "UserName": "Willy"
            },
            {
                "Age": 25,
                "ID": 88,
                "Url": "http://blog.golang.org/nutter",
                "UserName": "Nutter"
            },
            {
                "Age": 33,
                "ID": 89,
                "Url": "http://blog.golang.org/Pigg",
                "UserName": "Pigg"
            },
            {
                "Age": 22,
                "ID": 90,
                "Url": "http://blog.golang.org/cock",
                "UserName": "Cock"
            },
            {
                "Age": 22,
                "ID": 91,
                "Url": "http://blog.golang.org/cock",
                "UserName": "Cock"
            },
            {
                "Age": 21,
                "ID": 92,
                "Url": "http://blog.golang.org/hickinbottom",
                "UserName": "Hickinbottom"
            },
            {
                "Age": 22,
                "ID": 93,
                "Url": "http://blog.golang.org/willy",
                "UserName": "Willy"
            },
            {
                "Age": 25,
                "ID": 94,
                "Url": "http://blog.golang.org/nutter",
                "UserName": "Nutter"
            },
            {
                "Age": 33,
                "ID": 95,
                "Url": "http://blog.golang.org/Pigg",
                "UserName": "Pigg"
            },
            {
                "Age": 22,
                "ID": 98,
                "Url": "http://blog.golang.org/cock",
                "UserName": "Cock"
            },
            {
                "Age": 22,
                "ID": 99,
                "Url": "http://blog.golang.org/cock",
                "UserName": "Cock"
            },
            {
                "Age": 21,
                "ID": 100,
                "Url": "http://blog.golang.org/hickinbottom",
                "UserName": "Hickinbottom"
            },
            {
                "Age": 22,
                "ID": 101,
                "Url": "http://blog.golang.org/willy",
                "UserName": "Willy"
            },
            {
                "Age": 25,
                "ID": 102,
                "Url": "http://blog.golang.org/nutter",
                "UserName": "Nutter"
            },
            {
                "Age": 33,
                "ID": 103,
                "Url": "http://blog.golang.org/Pigg",
                "UserName": "Pigg"
            }
        ]
    },
    "msg": "Success"
}
s = session()


if __name__ == '__main__':
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()



    # user_json = UserJson()
    # user_json.content = data
    # session.add(user_json)
    # session.commit()
    # user_jsons = s.query(UserJson).all()
    # for user_json in user_jsons:
    #     data['code'] = data['code'] + 1
    #     user_json.content = data

    subquery = session.query(UserJson.id.label('user_json_id'),
                       func.json_array_elements(UserJson.content['data']['users']).label('users')).subquery()
    query = session.query(UserJson.id, subquery.c.users).filter(subquery.c.users.op('->>')('Age').cast(Integer) >= 25,
                UserJson.id == subquery.c.user_json_id)
    count = 0

    for item in query.all():
        count += 1
        print(item)

    print(count)


    # query = session.query(UserJson.content.op('->>')('code')).filter(UserJson.content.op('->>')('code').cast(Integer) == 1).all()
    # for item in query:
    #     print(item)

    session.commit()

# user_json = UserJson()
# user_json.content = data
# s.add(user_json)
# s.commit()
# user_jsons = s.query(UserJson).all()
# for user_json in user_jsons:
#     data['code'] = data['code'] + 1
#     user_json.content = data
#
# s.commit()

# 单个查询
# query = s.query(UserJson.content.op('->>')('code')).filter(UserJson.content.op('->>')('code').cast(Integer) == 1).all()
# for item in query:
#     print(item)

"""
列表查询
"""
# subquery = s.query(UserJson.id.label('user_json_id'),
#                    func.json_array_elements(UserJson.content['data']['users']).label('users')) \
#     .subquery()
# query = s.query(UserJson.id, subquery.c.users) \
#     .filter(subquery.c.users.op('->>')('Age').cast(Integer) >= 25,
#             UserJson.id == subquery.c.user_json_id)
# count = 0
#
# for item in query.all():
#     count += 1
#     print(item)
#
# print(count)