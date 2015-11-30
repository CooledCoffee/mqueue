# -*- coding: utf-8 -*-
from mqueue import util
from mqueue.decorators import Task, Cron, Async
from mqueue.schedules import Minutely, Hourly, Daily, Weekly, Monthly, Yearly, \
    Minutes, Hours, Days, Months, Weekday

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

async = Async
task = Task
cron = Cron

init = util.init
start = util.start
