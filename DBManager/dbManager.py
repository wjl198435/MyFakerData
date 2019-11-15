import sys
sys.path.append("..")

# from createTables import getSession
from DBManager.createTables import getSession

class DBManager(object):
    def __init__(self):
        # Session = sessionmaker(bind=engine)
        self.session = getSession()

    def InsertOne(self,data):
        self.session.add(data)
        self.session.commit()

    def InsertAll(self,datas):
        self.session.add_all(datas)
        self.session.commit()