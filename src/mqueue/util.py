# -*- coding: utf-8 -*-
from decorated.util import modutil
from loggingd import log_enter, log_return, log_error
from threading import Thread
import doctest
import importlib
import loggingd
import signal
import time

log = loggingd.getLogger(__name__)

class Timer(Thread):
    error_delay = 60
    interval = None
    
    def __init__(self):
        super(Timer, self).__init__()
        self._exiting = False
        
    def run(self):
        self._init()
        while not self._exiting:
            self._sleep(self.interval)
            try:
                self._run()
            except Exception:
                log.warn('Timer failed.', exc_info=True)
                self._sleep(self.error_delay)
            
    def stop(self):
        self._exiting = True
        self.join()
        
    def _init(self):
        pass
    
    def _run(self):
        raise NotImplemented()
    
    def _sleep(self, seconds):
        integer, fraction = int(seconds), seconds % 1
        for _ in range(integer):
            time.sleep(1)
            if self._exiting:
                return
        time.sleep(fraction)

def obj_from_path(path):
    '''
    >>> obj = obj_from_path('mqueue.util.obj_from_path')
    >>> type(obj)
    <type 'function'>
    >>> obj.__name__
    'obj_from_path'
    '''
    mod, attr = path.rsplit('.', 1)
    mod = importlib.import_module(mod)
    return getattr(mod, attr)

def obj_to_path(obj):
    '''
    >>> from mqueue.util import obj_to_path
    >>> obj_to_path(obj_to_path)
    'mqueue.util.obj_to_path'
    '''
    return obj.__module__ + '.' + obj.__name__

def init(queue):
    import mqueue
    mqueue.QUEUE = queue

@log_enter('Starting queue ...')
@log_return('Queue stopped.')
@log_error('Queue failed.', exc_info=True)
def start(queue, dao):
    from mqueue import db
    from mqueue.scheduler import SchedulerThread
    from mqueue.worker import WorkerThread
    
    init(queue)
    db.dao = dao
    modutil.load_tree('tasks')
    
    worker = WorkerThread()
    worker.start()
    scheduler = SchedulerThread()
    scheduler.start()
    
    _wait_for_exit()
    
    worker.stop()
    scheduler.stop()
    
def _wait_for_exit():
    def _exit(*args):
        pass
    signal.signal(signal.SIGINT, _exit)
    signal.signal(signal.SIGTERM, _exit)
    signal.pause()

if __name__ == '__main__':
    doctest.testmod()
    