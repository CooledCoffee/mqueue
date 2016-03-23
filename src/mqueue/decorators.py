# -*- coding: utf-8 -*-
from datetime import datetime, timedelta
from decorated import Function
from decorated.base.context import ctx
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
        
    def enqueue(self, *args, **kw):
        self.enqueue_with_options(args, kw, {})
        
    @log_return('Enqueued task {self.name}.')
    def enqueue_with_options(self, args, kwargs, options):
        args = self._resolve_args(*args, **kwargs)
        args = json.dumps(args)
        delay = options.get('delay', timedelta(seconds=0))
        if isinstance(delay, (int, float)):
            delay = timedelta(seconds=delay)
        eta = datetime.now() + delay
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
    def __init__(self, schedule, skip_if_scheduled=True):
        super(Cron, self).__init__()
        self.schedule = _parse_schedule(schedule)
        self._skip_if_scheduled = skip_if_scheduled
        
    def is_overdue(self, now, last):
        if not self.schedule.is_overdue(now, last):
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
    
    def _is_init_args(self, *args, **kw):
        return True
        
class Async(Function):
    def _call(self, *args, **kw):
        options = {'delay': self._delay}
        self.enqueue_with_options(args, kw, options)
        
    def _init(self, delay=0):
        super(Async, self)._init()
        self._delay = delay
        
def _parse_schedule(schedule):
    '''
    >>> from mqueue.schedules import Hourly
    >>> str(_parse_schedule(Hourly(30)))
    '30 * * * *'
    >>> str(_parse_schedule(Hourly))
    '0 * * * *'
    >>> str(_parse_schedule('30 * * * *'))
    '30 * * * *'
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
    