# -*- coding: utf-8 -*-
from datetime import datetime, timedelta
from decorated.base.context import ctx
from loggingd import log_enter, log_error, log_return
from mqueue import db, util
from mqueue.db import Task
from mqueue.decorators import Cron
from mqueue.util import Timer
import doctest
import json
import mqueue

DELAY = 3

class WorkerThread(Timer):
    def __init__(self):
        super(WorkerThread, self).__init__()
        self._empty = False
    
    @property
    def interval(self):
        return 10 if self._empty else 0
    
    @log_error('Worker failed.', exc_info=True)
    def _run(self):
        with db.dao.SessionContext():  # @UndefinedVariable
            task = _peek()
            if task is None:
                self._empty = True
            else:
                self._empty = False
                _run(task)

def _calc_delay(retries):
    '''
    >>> _calc_delay(1).total_seconds()
    60.0
    >>> _calc_delay(2).total_seconds()
    300.0
    >>> _calc_delay(10).total_seconds()
    43200.0
    '''
    countdown = 60 * pow(5, retries - 1)
    seconds = min(countdown, 43200)
    return timedelta(seconds=seconds)

def _peek():
    try:
        task = _try_peek()
    except Exception:
        task = None
    return task

@log_error('Failed to peek queue.', exc_info=True)
def _try_peek():
    return ctx.session.query(Task) \
            .filter(Task.queue == mqueue.QUEUE) \
            .filter(Task.eta <= datetime.now()) \
            .order_by(Task.eta) \
            .first()
            
def _run(task):
    try:
        _try_run(task)
        ctx.session.delete(task)
    except Exception:
        task.retries += 1
        task.eta = datetime.now() + _calc_delay(task.retries)

@log_enter('Running task {task.id} ({task.name}) ...')
@log_return('Task {task.id} ({task.name}) succeeded.')
@log_error('Failed to run task {task.id} ({task.name}).', exc_info=True)
def _try_run(task):
    with db.dao.SessionContext() as ctx:  # @UndefinedVariable
        target = util.obj_from_path(task.name)
        args = json.loads(task.args)
        ctx.task = {'model': task, 'target': target}
        target.execute(**args)
        
if __name__ == '__main__':
    doctest.testmod()
    