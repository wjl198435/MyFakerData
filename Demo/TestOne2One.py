from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy import Column, String, Integer, Text, ForeignKey, Table
from sqlalchemy.orm.collections import InstrumentedList
import random
from faker import Faker
faker = Faker(locale='zh_CN')

from config import DB_URL

database = 'Test'
engine = create_engine(DB_URL.format(database))
Base = declarative_base()

# class Parent(Base):
#     __tablename__ = 'parent'
#     id = Column(Integer, primary_key=True)
#     child = relationship("Child", uselist=False, back_populates="parent")
#
# class Child(Base):
#     __tablename__ = 'child'
#     id = Column(Integer, primary_key=True)
#     parent_id = Column(Integer, ForeignKey('parent.id'))
#     parent = relationship("Parent", back_populates="child")

#父表
class User(Base):
    __tablename__ = "user"
    id = Column(Integer , primary_key=True , autoincrement=True)
    name = Column(String(50) , nullable=False)



#从表
class Arctire(Base):
    __tablename__ = "arctire"
    id = Column(Integer , primary_key=True , autoincrement=True)
    title = Column(String(50) , nullable=False)

    uid = Column(Integer,ForeignKey("user.id"))
    author = relationship("User" , backref="arctires")

class UserInfo(Base):

    __tablename__ = 'userinfo'

    id = Column(Integer, primary_key=True)
    name = Column(String(64))

    user_id = Column(Integer, ForeignKey('user.id'))
    userinfo = relationship('User', backref='userinfo', uselist=False)

if __name__ == '__main__':
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()

    # user = User(name = "tom")
    # arctire1 = Arctire(title = "title 1")
    # arctire2 = Arctire(title = "title 2")
    user = User(name = "tom")
    arctire1 = Arctire(title = "title 1")
    arctire2 = Arctire(title = "title 2")

    userinfo1 = UserInfo(name = 'name1')

    user.arctires.append(arctire1)
    user.arctires.append(arctire2)
    user.userinfo.append(userinfo1)
    session.add(user)
    session.commit()


    # print(type(user.arctires))

    # session.commit()