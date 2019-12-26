import sys
sys.path.append("..")

# from createTables import getSession
# from DBManager.createIOTables import getIotDataBaseSession

class DBManager(object):
    def __init__(self,session):
        # Session = sessionmaker(bind=engine)
        self._session = session

    def InsertOne(self,data):
        self._session.add(data)
        self._session.commit()
        self._session.close()

    def InsertAll(self,datas):
        self._session.add_all(datas)
        self._session.commit()
        self._session.close()