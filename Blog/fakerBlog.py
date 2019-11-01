# coding: utf-8
from faker import Faker
from Blog.BlogSchema import User, Article
from Blog.BlogSchema import engine
from sqlalchemy.orm import sessionmaker
faker = Faker(locale='zh_CN')


def fakerUser(session,num=10):
    faker_users = [User(
        username=faker.name(),
        password=faker.word(),
        email=faker.email(),
    ) for i in range(10)]
    return faker_users

if __name__ == '__main__':
    # user = User()
    Session = sessionmaker(bind=engine)
    session = Session()

    ### CRUD-C

    # faker_users = fakerUser(session)
    # print(faker_users)
    # session.add_all(faker_users)
    #
    # faker_categories = [Category(name=faker.word()) for i in range(5)]
    # session.add_all(faker_categories)
    #
    # faker_tags = [Tag(name=faker.word()) for i in range(20)]
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
    #
    # session.commit()

    ### CRUD-R
    #如果我们知道用户id，就可以用get方法， filter_by用于按某一个字段过滤，而filter可以让我们按多个字段过滤，all则是获取所有。

    ### CRUD-U
    # a = session.query(Article).get(10)
    # a.title = 'My test blog post'
    # session.add(a)
    # session.commit()
    #
    # a = session.query(Article).get(10)
    # a.tags.append(Tag(name='python'))
    # session.add(a)
    # session.commit()


    ### CRUD-D

    a = session.query(Article).get(10)
    session.delete(a)
    session.commit()