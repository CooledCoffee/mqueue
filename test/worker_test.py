# -*- coding: utf-8 -*-
from datetime import datetime, timedelta
from mqueue import worker
from mqueue.db import Task as TaskModel
from mqueue.decorators import Task
from mqueue.worker import WorkerThread
from testutil import DbTestCase
import json

@Task
def foo(a, b=2):
    if b == 0:
        raise Exception()
    foo.result = a + b

class PeekTest(DbTestCase):
    def test_queue(self):
        # set up
        with self.mysql.dao.create_session() as session:
            session.add(TaskModel(args='{}', eta=datetime(2000, 1, 1), name='a.b.foo', queue='queue2', retries=0))
            session.add(TaskModel(args='{}', eta=datetime(2000, 1, 1), name='a.b.bar', queue='queue1', retries=0))
            
        # test
        with self.mysql.dao.SessionContext():
            task = worker._peek()
            self.assertEqual('a.b.bar', task.name)
            
    def test_eta(self):
        # set up
        with self.mysql.dao.create_session() as session:
            session.add(TaskModel(args='{}', eta=datetime(2000, 1, 2), name='a.b.foo', queue='queue1', retries=0))
            session.add(TaskModel(args='{}', eta=datetime(2000, 1, 1), name='a.b.bar', queue='queue1', retries=0))
            
        # test
        with self.mysql.dao.SessionContext():
            task = worker._peek()
            self.assertEqual('a.b.bar', task.name)
            
    def test_no_task(self):
        # set up
        self.patches.patch('mqueue.worker.DELAY', 0)
        
        # test
        with self.mysql.dao.SessionContext():
            task = worker._peek()
            self.assertIsNone(task)
            
class RunTest(DbTestCase):
    def test_success(self):
        # set up
        with self.mysql.dao.create_session() as session:
            session.add(TaskModel(args=json.dumps({'a': 1, 'b': 3}), eta=datetime(2000, 1, 1), name='worker_test.foo', queue='queue1', retries=0))
            
        # test
        worker = WorkerThread()
        worker._empty = True
        worker._run()
        
        # verify
        self.assertEqual(4, foo.result)
        with self.mysql.dao.create_session() as session:
            self.assertEqual(0, session.query(TaskModel).count())
        self.assertFalse(worker._empty)
            
    def test_error(self):
        # set up
        with self.mysql.dao.create_session() as session:
            session.add(TaskModel(args=json.dumps({'a': 1, 'b': 0}), eta=datetime(2000, 1, 1), name='queue_test.worker_test.foo', queue='queue1', retries=0))
            
        # test
        worker = WorkerThread()
        worker._empty = True
        worker._run()
        
        # verify
        with self.mysql.dao.create_session() as session:
            task = session.query(TaskModel).one()
            self.assertEqual(1, task.retries)
            self.assertAlmostNow(task.eta - timedelta(minutes=1))
            
    def test_empty(self):
        # test
        worker = WorkerThread()
        worker._empty = False
        worker._run()
        
        # verify
        with self.mysql.dao.create_session() as session:
            self.assertEqual(0, session.query(TaskModel).count())
        self.assertTrue(worker._empty)
        