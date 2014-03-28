# -*- coding: utf-8 -*-

QUEUE = None

from mqueue.decorators import Task, Cron, Delay
from mqueue import crons, util

MINUTELY = crons.MINUTELY
HOURLY = crons.HOURLY
DAILY = crons.DAILY
WEEKLY = crons.WEEKLY
MONTHLY = crons.MONTHLY
MINUTES = crons.MINUTES
HOURS = crons.HOURS
DAYS = crons.DAYS

Delay = Delay
task = Task
cron = Cron

init = util.init
start = util.start
