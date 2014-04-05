# -*- coding: utf-8 -*-
from crontab import CronTab
from datetime import datetime, timedelta
from decorated import Function
from decorated.base.context import Context, ctx, ContextError
from loggingd import log_return
from mqueue import util
from mqueue.db import Task as TaskModel
import json
import mqueue

crons = []

class Task(Function):
    @property
    def name(self):
        return util.obj_to_path(self._func)
        
    @log_return('Enqueued task {self.name}.')
    def enqueue(self, *args, **kw):
        args = self._resolve_args(*args, **kw)
        args = json.dumps(args)
        eta = datetime.now() + Delay.value()
        model = TaskModel(
            args=args,
            eta=eta,
            name=self.name,
            queue=mqueue.QUEUE,
            retries=0
        )
        ctx.session.add(model)
            
class Cron(Task):
    def is_overdue(self, last):
        delta = self._schedule.next(last)
        delta = timedelta(seconds=delta)
        return last + delta < datetime.now()
    
    def _decorate(self, func):
        crons.append(self)
        return super(Cron, self)._decorate(func)
    
    def _init(self, schedule):
        super(Cron, self)._init()
        self._schedule = CronTab(schedule)
    
class Delay(Context):
    @staticmethod
    def value():
        zero_delay = timedelta(minutes=0)
        try:
            return ctx.dict().get('delay', zero_delay)
        except ContextError:
            return zero_delay
    
    def __init__(self, delay):
        super(Delay, self).__init__(delay=delay)
        