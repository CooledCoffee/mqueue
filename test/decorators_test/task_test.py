# -*- coding: utf-8 -*-
from datetime import timedelta
from mqueue.db import Task as TaskModel
from mqueue.decorators import Task, Delay
from testutil import DbTestCase
import json

@Task
def foo(a, b=2):
    pass

class EnqueueTest(DbTestCase):
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
            
    def test_with_delay(self):
        # test
        delay = timedelta(minutes=5)
        with self.mysql.dao.SessionContext():
            with Delay(delay):
                foo.enqueue(1, b=3)
        
        # verify
        with self.mysql.dao.create_session() as session:
            task = session.query(TaskModel).one()
            self.assertAlmostNow(task.eta - delay)
            