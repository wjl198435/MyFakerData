import sys
sys.path.append("..")

import datetime
from utils.logger import info, setInfo,debug
from Scheduler.scheduler import SchedulerEngine
from DBManager.CrawlPigPrice import PigPrice

class SchedulerManager(object):

    def __init__(self, serverclient):
        debug("SchedulerManager------------------")
        debug(serverclient)
        self.cloudClient = serverclient
        self.schedulerEngine = SchedulerEngine(self, 'client_scheduler')
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
        event = {'id':'jobs_report', 'title':'jobs_report', 'actions':['self.get_events_task'], 'config':{'type':'interval','unit':'minute', 'interval':5,'start_date':now}}
        return event


    def add_scheduled_event(self,event,insert=True):
        debug("add_scheduled_event")
        self.schedulerEngine.add_scheduled_event(event, False)

    def get_events_task(self):
        events = self.schedulerEngine.get_scheduled_events()
        self.cloudClient.EnqueuePacket(self.schedulerEngine.get_scheduled_events(),"test")
        print("get_events_task- events--->{}".format(events))

    def pig_price_task(self):
        pp = PigPrice()
        pp.getPigPrice()

    def get_events(self):
        debug("get_events---------------")

    def SendNotification(self, notification):
        debug('SendNotification: ' + notification)

    def RunAction(self, action):
        debug('RunAction:' + action)
        eval(action)()
        # action()
        # partial(action)
        # job()
        # self.actions_ran.append(action)
        # info(self.actions_ran)
        return True


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
        start_time  =  datetime.datetime.strftime(next_time,'%Y-%m-%dT%H:%M:%S.%fZ')

        pig_price_event = {'id':'getPigPrice', 'title':'pig_price_task', 'actions':['self.pig_price_task'], 'config':{'type':'interval','unit':'hour', 'interval':1,'start_date':start_time}}
        return pig_price_event
