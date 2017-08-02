# -*- coding: utf-8 -*-
from datetime import timedelta
from mqueue.db import TaskModel
from mqueue.decorators import Task
from testutil import DbTestCase
import json

@Task
def foo(a, b=2):
    pass

class EnqueueWithOptionsTest(DbTestCase):
    def test_normal(self):
        # test
        with self.mysql.dao.SessionContext():
            foo.enqueue(1, b=3)
        
        # verify
        with self.mysql.dao.create_session() as session:
            task = session.query(TaskModel).one()
            self.assertEqual({'a': 1, 'b': 3}, json.loads(task.args))
            self.assertAlmostNow(task.eta)
            self.assertEqual('decorators_test.task_test.foo', task.name)
            self.assertEqual('queue1', task.queue)
            self.assertEqual(0, task.retries)
            
    def test_timedelta_delay(self):
        # test
        with self.mysql.dao.SessionContext():
            foo.enqueue_with_options([1], {'b': 3}, {'delay': timedelta(minutes=5)})
        
        # verify
        with self.mysql.dao.create_session() as session:
            task = session.query(TaskModel).one()
            self.assertAlmostNow(task.eta - timedelta(minutes=5))
            
    def test_int_delay(self):
        # test
        with self.mysql.dao.SessionContext():
            foo.enqueue_with_options([1], {'b': 3}, {'delay': 300})
        
        # verify
        with self.mysql.dao.create_session() as session:
            task = session.query(TaskModel).one()
            self.assertAlmostNow(task.eta - timedelta(minutes=5))
            