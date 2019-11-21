import sys
sys.path.append("..")

import datetime
from utils.logger import info, setInfo,debug
from DBManager.createBigDataTables import PigPriceTable

# from DBManager.CrawlPigPrice import get_pig_price

class SchedulerManager(object):
    def __init__(self, client):
        debug("SchedulerManager")
        self.cloudClient = client
        self.schedulerEngine = client.schedulerEngine

        self.add_events()

    def job(self,message='stuff'):
        print("I'm working on:", message)

    def add_events(self):
        debug("add_events")
        pp_event = self.make_pig_price_event()
        self.add_scheduled_event(pp_event)

        test_event = self.make_test_seconds_event()
        self.add_scheduled_event(test_event)



    def make_test_seconds_event(self):
        now = datetime.datetime.strftime(datetime.datetime.utcnow(), '%Y-%m-%dT%H:%M:%S.%fZ')
        event = {'id':'testSeconds', 'title':'test_seconds', 'actions':['get_pig_price'], 'config':{'type':'interval','unit':'second', 'interval':5,'start_date':now}}
        return event

    def make_pig_price_event(self):
        debug("make_pig_price_event")
        now_time = datetime.datetime.utcnow()
        # 获取明天时间
        next_time = now_time + datetime.timedelta(days=+1)
        next_year = next_time.date().year
        next_month = next_time.date().month
        next_day = next_time.date().day
        # 获取明天3点时间
        next_time = datetime.datetime.strptime(str(next_year)+"-"+str(next_month)+"-"+str(next_day)+" 00:00:00", "%Y-%m-%d %H:%M:%S")
        start_time = price_job_every_day_at3am =  datetime.datetime.strftime(next_time,'%Y-%m-%dT%H:%M:%S.%fZ')

        pig_price_event = {'id':'getPigPrice', 'title':'getPigPrice', 'actions':['getPigPrice'], 'config':{'type':'interval','unit':'day', 'interval':1,'start_date':start_time}}
        return pig_price_event

    def add_scheduled_event(self,event,insert=True):
        debug("add_scheduled_event")
        self.schedulerEngine.add_scheduled_event(event, True)

