# -*- coding: utf-8 -*-
from datetime import datetime
from loggingd import log_error
from mqueue import db, decorators
from mqueue.db import Cron as CronModel
from mqueue.util import Timer
import mqueue

class SchedulerThread(Timer):
    interval = 20
    
    @log_error('Scheduler failed.', exc_info=True)
    def _run(self):
        for cron in decorators.crons:
            _check(cron)
    
@log_error('Failed to check cron {cron.name}.', exc_info=True)
def _check(cron):
    with db.dao.SessionContext() as ctx:  # @UndefinedVariable
        model = ctx.session.get_or_create(CronModel, mqueue.QUEUE, cron.name)
        if model.last is None or cron.is_overdue(model.last):
            cron.enqueue()
        model.last = datetime.now()
