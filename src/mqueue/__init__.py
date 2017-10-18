# -*- coding: utf-8 -*-
import signal
from decorated.util import modutil
from loggingd import log_enter, log_return, log_error

from mqueue import util
from mqueue.decorators import Async, Cron, Task
from mqueue.schedules import Daily, Days, Hourly, Hours, Minutely, Minutes, Monthly, Months, Weekday, Weekly, Yearly

QUEUE = None

MINUTELY = Minutely
HOURLY = Hourly
DAILY = Daily
WEEKLY = Weekly
MONTHLY = Monthly
YEARLY = Yearly
MINUTES = Minutes
HOURS = Hours
DAYS = Days
MONTHS = Months
WEEKDAY = Weekday

async = Async # pylint: disable=invalid-name
task = Task # pylint: disable=invalid-name
cron = Cron # pylint: disable=invalid-name

init = util.init

@log_enter('Starting queue ...')
@log_return('Queue stopped.')
@log_error('Queue failed.', exc_info=True)
def start(queue, dao, package='tasks'):
    from mqueue import db
    from mqueue.scheduler import SchedulerThread
    from mqueue.worker import WorkerThread

    init(queue)
    db.dao = dao
    modutil.load_tree(package)

    worker = WorkerThread()
    worker.start()
    scheduler = SchedulerThread()
    scheduler.start()

    _wait_for_exit()

    worker.stop()
    scheduler.stop()

def _wait_for_exit():
    def _exit(*args): # pylint: disable=unused-argument
        pass
    signal.signal(signal.SIGINT, _exit)
    signal.signal(signal.SIGTERM, _exit)
    signal.pause()
