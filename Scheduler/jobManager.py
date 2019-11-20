import datetime
import threading
import time
import logging

from datetime import  timedelta

_LOGGER = logging.getLogger(__name__)

import sys
sys.path.append("..")

from utils.logger import info, setInfo

from scheduler import SchedulerEngine
from Tasks.crawlPigPrice import getPigPrice



# import doJob.crawlPrice

def job(message='stuff'):
    print("I'm working on:", message)



class Client():
    def __init__(self):
        info('TestClient init')
        self.actions_ran = []

    def RunAction(self, action):
        info('RunAction:' + action)
        eval(action)()
        # action()
        # partial(action)
        # job()
        # self.actions_ran.append(action)
        # info(self.actions_ran)
        return True

    def SendNotification(self, notification):
        info('SendNotification: ' + notification)


class TestScheduler():
    def __init__(self):
        self.maxDiff = None
        self.test_client = Client()
        self.test_engine = SchedulerEngine(self.test_client, 'cayennemqtt_test.py')
        self.schedule_events = []

    def remove_schedules(self, engine=None):
        scheduled_events = {event['id']:event for event in self.schedule_events if 'id' in event}
        for event in scheduled_events.values():
            self.assertTrue(self.test_engine.remove_scheduled_event(event))

    def add_schedules(self, schedule_events):
        for event in schedule_events:
            self.test_engine.add_scheduled_event(event, True)
        self.schedule_events = self.schedule_events + schedule_events

    def check_schedules_added(self, expected):
        actual = self.test_engine.get_scheduled_events()
        # self.assertCountEqual(expected, actual)
        return actual

    def check_schedules_run(self, expected, skip_jobs=()):
        print('Pause to allow scheduled events to execute')
        expected_to_run = [action for event in expected if event['title'] not in skip_jobs for action in event['actions']]
        for i in range(70):
            time.sleep(1)
            if len(expected_to_run) > 0 and len(expected_to_run) == len(self.test_client.actions_ran):
                break
        # self.assertCountEqual(expected_to_run, self.test_client.actions_ran)
        return len(expected_to_run) == len(self.test_client.actions_ran)

    def __del__(self):
        self.remove_schedules()
        self.test_engine.stop()

    def test_concurrent_updates(self):
        # now = datetime.datetime.strftime(datetime.datetime.utcnow(), '%Y-%m-%dT%H:%M:%S.%fZ')
        # now = datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%dT%H:%M:%S.%fZ')
        # now = datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%dT%H:%M:%S.%fZ')

        # 获取现在时间
        now_time = datetime.datetime.utcnow()
        # 获取明天时间
        next_time = now_time + datetime.timedelta(days=+1)
        next_year = next_time.date().year
        next_month = next_time.date().month
        next_day = next_time.date().day
        # 获取明天3点时间
        next_time = datetime.datetime.strptime(str(next_year)+"-"+str(next_month)+"-"+str(next_day)+" 00:00:00", "%Y-%m-%d %H:%M:%S")



        info("utcnow:"+str(datetime.datetime.utcnow()))

        info("next_time: "+str(next_time))

        #
        # info(datetime.datetime.utcnow()-datetime.timedelta(hours=6))
        #
        # start_get_pig_price_time_job = datetime.datetime.utcnow() - datetime.timedelta(hours=6)
        price_job_every_day_at3am =  datetime.datetime.strftime(next_time,'%Y-%m-%dT%H:%M:%S.%fZ')
        schedule_events = [
            {'id':'getPigPrice', 'title':'getPigPrice', 'actions':['job'], 'config':{'type':'interval','unit':'day', 'interval':1,'start_date':price_job_every_day_at3am}},
            # {'id':'testSeconds', 'title':'test_seconds', 'actions':['job'], 'config':{'type':'interval','unit':'second', 'interval':10,'start_date':now}},


            # {'id':'concurrent_1', 'title':'date_job', 'actions':['job'], 'config':{'type':'interval', 'start_date':now}},
            # {'id':'concurrent_10', 'title':'seconds_job_updated', 'actions':['job'], 'config':{'type':'interval','unit':'second', 'interval':3,'start_date':now}},

            # {'id':'concurrent_20', 'title':'minutes_job_updated', 'actions':['job'], 'config':{'type':'interval','unit':'minute', 'interval':1,'start_date':now}},
            # {'id':'concurrent_20', 'title':'daily_job_updated', 'actions':['daily_job_action'], 'config':{'type':'interval', 'unit':'day', 'interval':1, 'start_date':now}},
            # {'id':'concurrent_3', 'title':'weekly_job', 'actions':['weekly_job_action'], 'config':{'type':'interval', 'unit':'week', 'interval':1, 'start_date':now}},
            # {'id':'concurrent_30', 'title':'weekly_job_updated', 'actions':['weekly_job_action'], 'config':{'type':'interval', 'unit':'week', 'interval':1, 'start_date':now}},
            # {'id':'concurrent_4', 'title':'monthly_job', 'actions':['monthly_job_action'], 'config':{'type':'interval', 'unit':'month', 'interval':1, 'start_date':now}},
            # {'id':'concurrent_40', 'title':'monthly_job_updated', 'actions':['monthly_job_action'], 'config':{'type':'interval', 'unit':'month', 'interval':1, 'start_date':now}},
            # {'id':'concurrent_5', 'title':'yearly_job', 'actions':['yearly_job_action'], 'config':{'type':'interval', 'unit':'year', 'interval':1, 'start_date':now}},
            # {'id':'concurrent_50', 'title':'yearly_job_updated', 'actions':['yearly_job_action'], 'config':{'type':'interval', 'unit':'year', 'interval':1, 'start_date':now}}
        ]
        for event in schedule_events:
            threading.Thread(target=self.add_schedules, daemon=True, args=([event],)).start()
        #Only half the schedule_events should run since ones with the same id will overwrite previously added ones. Since we don't know what order that will take
        #we just make sure we only check that one of each action has run.
        run_events = {event['id']:event for event in schedule_events if 'id' in event}
        skip_jobs = [event['title'] for event in run_events.values()]
        self.check_schedules_run(schedule_events, skip_jobs)

if __name__ == '__main__':
    setInfo()
    ts = TestScheduler()
    now = datetime.datetime.strftime(datetime.datetime.utcnow(), '%Y-%m-%dT%H:%M:%S.%fZ')

    ts.test_concurrent_updates()

    # now = datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%dT%H:%M:%S.%fZ')
    # print(now)