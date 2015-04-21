# -*- coding: utf-8 -*-
from datetime import datetime, timedelta
from decorated import Function
from decorated.base.context import Context, ctx, ContextError
from loggingd import log_return
from mqueue import util
from mqueue.db import Task as TaskModel
from mqueue.schedules import CronSchedule, Schedule
import doctest
import json
import mqueue

NO_DELAY = timedelta(minutes=0)
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
        
    def execute(self, *args, **kw):
        return self._call(*args, **kw)
    
class Cron(Task):
    def __init__(self, *args, **kw):
        super(Cron, self).__init__(*args, **kw)
        self._decorate_or_call = self._decorate
        self._init(*args, **kw)
            
    def is_overdue(self, now, last):
        if not self._schedule.is_overdue(now, last):
            return False
        if self._skip_if_scheduled:
            cnt = ctx.session.query(TaskModel) \
                    .filter(TaskModel.name == self.name) \
                    .count()
            if cnt > 0:
                return False
        return True
    
    def _decorate(self, func):
        crons.append(self)
        return super(Cron, self)._decorate(func)
    
    def _init(self, schedule, skip_if_scheduled=True):
        super(Cron, self)._init()
        self._schedule = _parse_schedule(schedule)
        self._skip_if_scheduled = skip_if_scheduled
        
    def _is_init_args(self, *args, **kw):
        return True
    
class Delay(Context):
    @staticmethod
    def value():
        try:
            return ctx.dict().get('mqueue.delay', NO_DELAY)
        except ContextError:
            return NO_DELAY
    
    def __init__(self, delay):
        super(Delay, self).__init__()
        self['mqueue.delay'] = delay
        
class Async(Function):
    def _call(self, *args, **kw):
        if self._delay is None:
            return self.enqueue(*args, **kw)
        else:
            with Delay(self._delay):
                return self.enqueue(*args, **kw)
        
    def _init(self, delay=None):
        super(Async, self)._init()
        self._delay = delay
        
def _parse_schedule(schedule):
    '''
    >>> from mqueue.schedules import Hourly
    >>> str(_parse_schedule(Hourly(30)))
    'CronSchedule(30 * * * *)'
    >>> str(_parse_schedule(Hourly))
    'CronSchedule(0 * * * *)'
    >>> str(_parse_schedule('30 * * * *'))
    'CronSchedule(30 * * * *)'
    >>> str(_parse_schedule(30))
    Traceback (most recent call last):
    ...
    Exception: Bad schedule "30".
    '''
    if isinstance(schedule, Schedule):
        return schedule
    elif callable(schedule):
        return schedule()
    elif isinstance(schedule, basestring):
        return CronSchedule(schedule)
    else:
        raise Exception('Bad schedule "%s".' % schedule)

if __name__ == '__main__':
    doctest.testmod()
    