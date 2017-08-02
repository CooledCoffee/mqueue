# -*- coding: utf-8 -*-
from datetime import datetime

from loggingd import log_error

from mqueue import db, decorators, util
from mqueue.db import CronModel
from mqueue.util import Timer


class SchedulerThread(Timer):
    @property
    def interval(self):
        return 60 - datetime.now().second + 1
    
    @log_error('Failed to sync cron table.', exc_info=True)
    def _init(self):
        valid_names = {cron.name for cron in decorators.crons}
        with db.dao.create_session() as session:  # @UndefinedVariable
            models = session.query(CronModel) \
                    .filter(CronModel.queue == util.QUEUE) \
                    .all()
            for model in models:
                if model.name not in valid_names:
                    session.delete(model)
            for cron in decorators.crons:
                model = session.get_or_create(CronModel, util.QUEUE, cron.name)
                model.schedule = str(cron.schedule)
    
    @log_error('Scheduler failed.', exc_info=True)
    def _run(self):
        now = datetime.now()
        for cron in decorators.crons:
            _check(cron, now)
    
@log_error('Failed to check cron {cron.name}.', exc_info=True)
def _check(cron, now):
    with db.dao.SessionContext() as ctx:
        model = ctx.session.get(CronModel, util.QUEUE, cron.name)
        if model.last is None or cron.is_overdue(now, model.last):
            cron.enqueue()
            model.last = now
