# -*- coding: utf-8 -*-
from datetime import datetime, timedelta
from mqueue.db import TaskModel
from mqueue.decorators import Async, Task
from testutil import DbTestCase

class AsyncTest(DbTestCase):
    def test_basic(self):
        # set up
        @Async
        @Task
        def foo(a, b=0):
            pass
        
        # test
        with self.mysql.dao.SessionContext():
            foo(1, b=2)
            
        # verify
        with self.mysql.dao.create_session() as session:
            self.assertEqual(1, session.query(TaskModel).count())
            
    def test_with_delay(self):
        # set up
        @Async(delay=timedelta(seconds=300))
        @Task
        def foo(a, b=0):
            pass
        
        # test
        with self.mysql.dao.SessionContext():
            foo(1, b=2)
            
        # verify
        with self.mysql.dao.create_session() as session:
            model = session.query(TaskModel).one()
            self.assertGreater(model.eta, datetime.now())
            