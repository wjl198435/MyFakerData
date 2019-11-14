"""
Python job scheduling for humans.
An in-process scheduler for periodic jobs that uses the builder pattern
for configuration. Schedule lets you run Python functions (or any other
callable) periodically at pre-determined intervals using a simple,
human-friendly syntax.
Inspired by Addam Wiggins' article "Rethinking Cron" [1] and the
"clockwork" Ruby module [2][3].
Features:
    - A simple to use API for scheduling jobs.
    - Very lightweight and no external dependencies.
    - Excellent jobManager.py coverage.
    - Works with Python 2.7 and 3.3
Usage:
    >>> import schedule
    >>> import time
    >>> def job(message='stuff'):
    >>>     print("I'm working on:", message)
    >>> schedule.every(10).minutes.do(job)
    >>> schedule.every().hour.do(job, message='things')
    >>> schedule.every().day.at("10:30").do(job)
    >>> while True:
    >>>     schedule.run_pending()
    >>>     time.sleep(1)
[1] http://adam.heroku.com/past/2010/4/13/rethinking_cron/
[2] https://github.com/tomykaira/clockwork
[3] http://adam.heroku.com/past/2010/6/30/replace_cron_with_clockwork/
"""
from datetime import datetime, timedelta
import functools

import time
import math
import calendar
from logger import  error, exception, info, logJson, setDebug, warn

class CancelJob(object):
    pass


class Scheduler(object):
    def __init__(self):
        self.jobs = []

    def run_pending(self):
        """Run all jobs that are scheduled to run.
        Please note that it is *intended behavior that tick() does not
        run missed jobs*. For example, if you've registered a job that
        should run every minute and you only call tick() in one hour
        increments then your job won't be run 60 times in between but
        only once.
        """
        runnable_jobs = (job for job in self.jobs if job.should_run)
        for job in sorted(runnable_jobs):
            self._run_job(job)

    def run_all(self, delay_seconds=0):
        """Run all jobs regardless if they are scheduled to run or not.
        A delay of `delay` seconds is added between each job. This helps
        distribute system load generated by the jobs more evenly
        over time."""
        #info('Running *all* %i jobs with %is delay inbetween',len(self.jobs), delay_seconds)
        for job in self.jobs:
            self._run_job(job)
            time.sleep(delay_seconds)

    def clear(self):
        """Deletes all scheduled jobs."""
        del self.jobs[:]

    def cancel_job(self, job):
        """Delete a scheduled job."""
        try:
            self.jobs.remove(job)
        except ValueError:
            pass

    def every(self, interval=1, start_date=None):
        """Schedule a new periodic job."""
        job = Job(interval, start_date)
        self.jobs.append(job)
        return job

    def once(self):
        """Schedule a new job to run once."""
        job = Job(0)
        self.jobs.append(job)
        return job

    def _run_job(self, job):
        ret = job.run()
        if isinstance(ret, CancelJob) or ret is CancelJob:
            self.cancel_job(job)

    @property
    def next_run(self):
        """Datetime when the next job should run."""
        if not self.jobs:
            return None
        return min(self.jobs).next_run

    @property
    def idle_seconds(self):
        """Number of seconds until `next_run`."""
        return (self.next_run - datetime.utcnow()).total_seconds()


class Job(object):
    """A job as used by `Scheduler`."""
    def __init__(self, interval, start_date = None):
        self.interval = interval  # pause interval * unit between runs
        self.job_func = None  # the job job_func to run
        self.unit = None  # time units, e.g. 'minutes', 'hours', ...
        if interval == 0:
            self.unit = 'date'
        self.at_time = None  # optional time at which this job runs
        self.last_run = None  # datetime of the last run
        self.next_run = None  # datetime of the next run
        self.period = None  # timedelta between runs, only valid for
        self.start_day = None  # Specific day of the week to start on
        self.end_date = None # Set end date for this job
        self.start_date = start_date # Set start date for this job
        self.grace_period = timedelta(seconds=60)

    def __lt__(self, other):
        """PeriodicJobs are sortable based on the scheduled time
        they run next."""
        return self.next_run < other.next_run

    def __repr__(self):
        def format_time(t):
            return t.strftime('%Y-%m-%d %H:%M:%S') if t else '[never]'

        timestats = '(last run: %s, next run: %s)' % (
            format_time(self.last_run), format_time(self.next_run))

        if hasattr(self.job_func, '__name__'):
            job_func_name = self.job_func.__name__
        else:
            job_func_name = repr(self.job_func)
        args = [repr(x) for x in self.job_func.args]
        kwargs = ['%s=%s' % (k, repr(v))
                  for k, v in self.job_func.keywords.items()]
        call_repr = job_func_name + '(' + ', '.join(args + kwargs) + ')'

        if self.unit == 'date':
            return 'At %s do %s %s' % (
                self.at_time, call_repr, timestats)
        if self.at_time is not None:
            return 'Every %s %s starting at %s do %s %s' % (
                self.interval,
                self.unit[:-1] if self.interval == 1 else self.unit,
                self.at_time, call_repr, timestats)
        else:
            return 'Every %s %s do %s %s' % (
                self.interval,
                self.unit[:-1] if self.interval == 1 else self.unit,
                call_repr, timestats)

    @property
    def second(self):
        assert self.interval == 1
        return self.seconds

    @property
    def seconds(self):
        self.unit = 'seconds'
        return self

    @property
    def minute(self):
        assert self.interval == 1
        return self.minutes

    @property
    def minutes(self):
        self.unit = 'minutes'
        return self

    @property
    def hour(self):
        assert self.interval == 1
        return self.hours

    @property
    def hours(self):
        self.unit = 'hours'
        return self

    @property
    def day(self):
        assert self.interval == 1
        return self.days

    @property
    def days(self):
        self.unit = 'days'
        return self

    @property
    def week(self):
        assert self.interval == 1
        return self.weeks

    @property
    def monday(self):
        assert self.interval == 1
        self.start_day = 'monday'
        return self.weeks

    @property
    def tuesday(self):
        assert self.interval == 1
        self.start_day = 'tuesday'
        return self.weeks

    @property
    def wednesday(self):
        assert self.interval == 1
        self.start_day = 'wednesday'
        return self.weeks

    @property
    def thursday(self):
        assert self.interval == 1
        self.start_day = 'thursday'
        return self.weeks

    @property
    def friday(self):
        assert self.interval == 1
        self.start_day = 'friday'
        return self.weeks

    @property
    def saturday(self):
        assert self.interval == 1
        self.start_day = 'saturday'
        return self.weeks

    @property
    def sunday(self):
        assert self.interval == 1
        self.start_day = 'sunday'
        return self.weeks

    @property
    def weeks(self):
        self.unit = 'weeks'
        return self

    @property
    def month(self):
        assert self.interval == 1
        return self.months

    @property
    def months(self):
        self.unit = 'months'
        return self

    @property
    def year(self):
        assert self.interval == 1
        return self.years

    @property
    def years(self):
        self.interval = self.interval
        self.unit = 'years'
        return self

    def at(self, time_str):
        """Schedule the job at a specific UTC time."""
        self.at_time = self.make_date(time_str)
        return self

    def make_date(self, datetime_str):
        """Make datetime from string."""
        try:
            date = datetime.strptime(datetime_str, '%Y-%m-%dT%H:%M:%S.%fZ')
        except ValueError:
            date = datetime.strptime(datetime_str, '%Y-%m-%d %H:%M')
        assert 0 <= date.hour <= 23
        assert 0 <= date.minute <= 59
        assert 1 <= date.day <= 31
        assert 1 <= date.month <= 12
        assert 2014 <= date.year
        return date

    def until(self, end_date):
        """Schedule the job until specific end date."""
        if end_date is not None:
            self.end_date = self.make_date(end_date)
        return self

    def do(self, job_func, *args, **kwargs):
        """Specifies the job_func that should be called every time the
        job runs.
        Any additional arguments are passed on to job_func when
        the job runs.
        """

        self.job_func = functools.partial(job_func, *args, **kwargs)
        # print(self.job_func)
        try:
            functools.update_wrapper(self.job_func, job_func)
        # except AttributeError:
        #     # job_funcs already wrapped by functools.partial won't have
        #     # __name__, __module__ or __doc__ and the update_wrapper()
        #     # call will fail.
        #     pass
        except Exception as e:
            print('str(Exception):\t', str(Exception))
            print('str(e):\t\t', str(e))
            print('repr(e):\t', repr(e))
            print('e.message:\t', e.message)
            print('traceback.print_exc():', traceback.print_exc())
            print('traceback.format_exc():\n%s' % traceback.format_exc())
        self._schedule_next_run()
        print('Do job, next run time: ' + str(self.next_run))
        return self

    def set_last_run(self, last_run):
        """Set the job's last run time."""
        if last_run is not None:
            self.last_run = self.make_date(last_run)
        return self

    @property
    def should_run(self):
        """True if the job should be run now."""
        return self.next_run is not None and datetime.utcnow() >= self.next_run

    def run(self):
        """Run the job and immediately reschedule it."""
        print('Run job')
        if self.unit == 'date':
            if self.last_run is not None:
                print('date job can run only once. Last run: ' + str(self.last_run))
                return CancelJob
            now = datetime.utcnow()
            #If more than the grace period has passed since the scheduled start time we cancel the job
            if now > (self.at_time + self.grace_period):
                print('Job scheduled time has passed, job will not be run: ' + str(self.at_time) + ' current time: ' + str(now))
                return CancelJob

        print('Running job: {}'.format(self))

        if self.end_date is not None:
            if datetime.utcnow() > self.end_date:
                print('Skipping job, end date has passed: ' + str(self.end_date))
                return CancelJob

        ret = self.job_func()
        self.last_run = datetime.utcnow()

        if self.unit == 'date':
            print('Date job finished, it will not be recheduled')
            return CancelJob

        self._schedule_next_run()
        print('Job finished, next run time: ' + str(self.next_run))

        return ret
    def run_available(self):
        if self.last_run == None:
            return True
        return self.last_run + self.period - timedelta(**{'seconds': 1}) < self.next_run
    def _schedule_next_run(self):
        """Compute the instant when this job should run next."""
        # Allow *, ** magic temporarily:
        # pylint: disable=W0142
        assert self.unit in ('seconds', 'minutes', 'hours', 'days', 'weeks', 'months', 'years', 'date')

        if self.unit == 'date' and self.at_time is not None:
            if self.last_run is not None:
                return
            if self.last_run is not None and self.next_run is not None and (self.last_run - self.next_run).total_seconds() > 0:
                print('Already run')
                return
            self.next_run = self.at_time
            return

        if self.unit in ('months', 'years'):
            if self.unit == 'years':
                interval_in_months = self.interval * 12
            else:
                interval_in_months = self.interval
            now = datetime.utcnow()
            elapsed_months = (12*(now.year - self.at_time.year) + now.month - self.at_time.month +
                              int(now.day > self.at_time.day) + int(self.at_time.day == now.day and now.time() > (self.at_time + self.grace_period).time()))
            if elapsed_months < 0:
                elapsed_months = 0
            elapsed_periods = math.ceil(elapsed_months / interval_in_months)
            self.next_run = month_delta(self.at_time, elapsed_periods * interval_in_months)
            if self.last_run and self.next_run <= (self.last_run + self.grace_period):
                self.next_run = month_delta(self.next_run, interval_in_months)
            return
        self.period = timedelta(**{self.unit: self.interval})
        self.next_run = datetime.utcnow() + self.period
        #todo: no 'minutes' implementation
        if self.unit in ('hours'):
            if self.start_date != None:
                try:
                    date = datetime.strptime(self.start_date, '%Y-%m-%dT%H:%M:%S.%fZ')
                except ValueError:
                    date = datetime.strptime(self.start_date, '%Y-%m-%d %H:%M')
                self.next_run = date
                #'2016-11-30 17:52'
                now = datetime.utcnow()
                if self.next_run < now:
                    oneDay = timedelta(**{'days': 1})
                    firstDate = now.replace(hour=self.next_run.hour, minute=self.next_run.minute) - oneDay #, second=0, microsecond=0
                    while firstDate < now:
                        firstDate = firstDate + self.period
                    if self.last_run != None and self.last_run + self.period - timedelta(**{'seconds': 1}) > self.next_run:
                        firstDate = firstDate + self.period
                    self.next_run = firstDate
        if self.start_day is not None:
            assert self.unit == 'weeks'
            weekdays = (
                'monday',
                'tuesday',
                'wednesday',
                'thursday',
                'friday',
                'saturday',
                'sunday'
            )
            assert self.start_day in weekdays
            weekday = weekdays.index(self.start_day)
            days_ahead = weekday - self.next_run.weekday()
            if days_ahead <= 0:  # Target day already happened this week
                days_ahead += 7
            self.next_run += timedelta(days_ahead) - self.period
        if self.at_time is not None:
            now = datetime.utcnow()
            elapsed_periods = math.ceil((now - (self.at_time + self.grace_period)) / self.period)
            if elapsed_periods < 0:
                elapsed_periods = 0
            self.next_run = self.at_time + (elapsed_periods * self.period)
            if self.last_run and self.next_run <= (self.last_run + self.grace_period):
                self.next_run += self.period
        if self.start_day is not None and self.at_time is not None:
            # Let's see if we will still make that time we specified today
            if (self.next_run - datetime.utcnow()).days >= 7:
                self.next_run -= self.period


# The following methods are shortcuts for not having to
# create a Scheduler instance:

default_scheduler = Scheduler()
jobs = default_scheduler.jobs  # todo: should this be a copy, e.g. jobs()?


def every(interval=1, start_date = None):
    """Schedule a new periodic job."""
    return default_scheduler.every(interval, start_date)


def once():
    """Schedule a new job to run once."""
    return default_scheduler.once()


def run_pending():
    """Run all jobs that are scheduled to run.
    Please note that it is *intended behavior that run_pending()
    does not run missed jobs*. For example, if you've registered a job
    that should run every minute and you only call run_pending()
    in one hour increments then your job won't be run 60 times in
    between but only once.
    """
    default_scheduler.run_pending()


def run_all(delay_seconds=0):
    """Run all jobs regardless if they are scheduled to run or not.
    A delay of `delay` seconds is added between each job. This can help
    to distribute the system load generated by the jobs more evenly over
    time."""
    default_scheduler.run_all(delay_seconds=delay_seconds)


def clear():
    """Deletes all scheduled jobs."""
    default_scheduler.clear()


def cancel_job(job):
    """Delete a scheduled job."""
    default_scheduler.cancel_job(job)


def next_run():
    """Datetime when the next job should run."""
    return default_scheduler.next_run


def idle_seconds():
    """Number of seconds until `next_run`."""
    return default_scheduler.idle_seconds


def month_delta(date, months):
    """Add or subtract months from date."""
    day = date.day
    # subtract one because months are not zero-based
    month = date.month + months - 1
    year = date.year + month // 12
    # now add it back
    month = month % 12 + 1
    days_in_month = calendar.monthrange(year, month)[1]
    if day >= days_in_month:
        day = days_in_month
    try:
        return date.replace(year, month, day)
    except ValueError:
        raise OverflowError('date value out of range')

def add_schedules(self, schedule_events):
    for event in schedule_events:
        self.test_engine.add_scheduled_event(event, True)
    self.schedule_events = self.schedule_events + schedule_events


if __name__ == '__main__':
    start_date = datetime.strftime(datetime.utcnow() + timedelta(seconds=60), '%Y-%m-%dT%H:%M:%S.%fZ')
    now = datetime.strftime(datetime.utcnow(), '%Y-%m-%dT%H:%M:%S.%fZ')
    schedule_events = [{'id':'current_1', 'title':'date_job', 'actions':['date_job_action'], 'config':{'type':'date', 'start_date':start_date}},
                       {'id':'current_2', 'title':'daily_job', 'actions':['daily_job_action'], 'config': {'type':'interval', 'unit':'day', 'interval':1, 'start_date':start_date}},
                       {'id':'current_3', 'title':'every_3_days_job', 'actions':['every_3_days_job_action'], 'config':{'type':'interval', 'unit':'day', 'interval':3, 'start_date':start_date}},
                       {'id':'current_4', 'title':'now_date_job', 'actions':['now_date_job_action'], 'config':{'type':'date', 'start_date':now}},
                       {'id':'current_5', 'title':'weekly_job', 'actions':['weekly_job_action'], 'config':{'type':'interval', 'unit':'week', 'interval':1, 'start_date':start_date}},
                       {'id':'current_6', 'title':'bi-weekly_job', 'actions':['weekly_job_action'], 'config':{'type':'interval', 'unit':'week', 'interval':2, 'start_date':start_date}},
                       {'id':'current_7', 'title':'every_4_months_job', 'actions':['every_4_months_job_action'], 'config':{'type':'interval', 'unit':'month', 'interval':4, 'start_date':start_date}},
                       {'id':'current_8', 'title':'every_3_months_job', 'actions':['every_3_months_job_action'], 'config':{'type':'interval', 'unit':'month', 'interval':3, 'start_date':now}},
                       {'id':'current_9', 'title':'hourly_job', 'actions':['hourly_job_action'], 'config': {'type':'interval', 'unit':'hour', 'interval':1, 'start_date':start_date}}]

    # print(schedule_events)

    schedule = Scheduler()

    def job(message='stuff'):
        print("I'm working on:", message)
    schedule.every(10).seconds.do(job)
    # schedule.every().hour.do(job, message='things')
    # schedule.every().day.at("10:30").do(job)
    while True:
        schedule.run_pending()
        time.sleep(1)