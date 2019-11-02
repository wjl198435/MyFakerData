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


    # scope = relationship('Scope', secondary='company_scope', backref='scopes')
    # work = relationship('User', backref='work')

    def __repr__(self):
        return '%s(%r,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)' \
               % (self.__class__.__name__, self.corporate,self.scale,self.total_scale,self.social_credit_issue,self.credit_rate,
                  self.lat,self.lon,self.link,self.license_id,self.province,self.city,self.street_address,self.company,self.address,self.contact)




# class Article(Base):
#
#     __tablename__ = 'articles'
#
#     id = Column(Integer, primary_key=True)
#     title = Column(String(255), nullable=False, index=True)
#     content = Column(Text)
#     user_id = Column(Integer, ForeignKey('users.id'))
#     cate_id = Column(Integer, ForeignKey('categories.id'))
#     tags = relationship('Tag', secondary='article_tag', backref='articles')
#
#     def __repr__(self):
#         return '%s(%r)' % (self.__class__.__name__, self.title)


# class Category(Base):
#
#     __tablename__ = 'categories'
#
#     id = Column(Integer, primary_key=True)
#     name = Column(String(64), nullable=False, index=True)
#     articles = relationship('Article', backref='category')
#
#     def __repr__(self):
#         return '%s(%r)' % (self.__class__.__name__, self.name)


# article_tag = Table(
#     'article_tag', Base.metadata,
#     Column('article_id', Integer, ForeignKey('articles.id')),
#     Column('tag_id', Integer, ForeignKey('tags.id'))
# )


# class Tag(Base):
#
#     __tablename__ = 'tags'
#
#     id = Column(Integer, primary_key=True)
#     name = Column(String(64), nullable=False, index=True)
#
#     def __repr__(self):
#         return '%s(%r)' % (self.__class__.__name__, self.name)


if __name__ == '__main__':
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()
    sum = 10


    companies = [Company(
        corporate = "法人",
        name=faker.company(),
    ) for i in range(sum)]

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


    faker_roles= [Role(name=random.choice(Roles)) for i in range(len(Roles))]
    # print(faker_roles)
    # faker_tags= [Tag(name=faker.word()) for i in range(20)]



    for i in range(sum):
        users[i].userinfo.append(userinfos[i])
        users[i].role = random.choice(faker_roles)
        users[i].company = random.choice(companies)

    session.add_all(users)



    # for i in range(sum):
    #     companies.users.append(users[i])



    # faker_categories = [Category(name=faker.word()) for i in range(5)]
    # session.add_all(faker_categories)
    #
    # faker_tags= [Tag(name=faker.word()) for i in range(20)]
    # session.add_all(faker_tags)
    #
    # for i in range(100):
    #     article = Article(
    #         title=faker.sentence(),
    #         content=' '.join(faker.sentences(nb=random.randint(10, 20))),
    #         author=random.choice(faker_users),
    #         category=random.choice(faker_categories)
    #     )
    #     for tag in random.sample(faker_tags, random.randint(2, 5)):
    #         article.tags.append(tag)
    #     session.add(article)

    session.commit()
