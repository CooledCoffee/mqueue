# -*- coding: utf-8 -*-
from datetime import datetime
from mqueue import decorators
from mqueue.db import Task
from mqueue.decorators import Cron
from mqueue.schedules import Hourly
from testutil import TestCase, DbTestCase

class DecorateTest(TestCase):
    def test(self):
        # set up
        self.patches.patch('mqueue.decorators.crons', [])
        
        # test
        @Cron('* * * * *')
        def foo():
            pass
        self.assertEqual(1, len(decorators.crons))
        self.assertEqual(foo, decorators.crons[0])
        
class IsOverdueTest(DbTestCase):
    def test_normal(self):
        @Cron(Hourly)
        def foo():
            pass
        with self.mysql.dao.SessionContext():
            self.assertTrue(foo.is_overdue(datetime(2000, 1, 1, 1, 0, 0), datetime(2000, 1, 1)))
            self.assertFalse(foo.is_overdue(datetime(2000, 1, 1, 0, 30, 0), datetime(2000, 1, 1)))
        
    def test_scheduled(self):
        # set up
        @Cron(Hourly)
        def foo():
            pass
        with self.mysql.dao.create_session() as session:
            session.add(Task(args='{}', eta=datetime(2000, 1, 1), name='decorators_test.cron_test.foo', queue='queue1', retries=0))
            
        # test
        with self.mysql.dao.SessionContext():
            self.assertFalse(foo.is_overdue(datetime(2000, 1, 2), datetime(2000, 1, 1)))
            
    def test_no_skip(self):
        # set up
        @Cron(Hourly, skip_if_scheduled=False)
        def foo():
            pass
        with self.mysql.dao.create_session() as session:
            session.add(Task(args='{}', eta=datetime(2000, 1, 1), name='decorators_test.cron_test.foo', queue='queue1', retries=0))
            
        # test
        with self.mysql.dao.SessionContext():
            self.assertTrue(foo.is_overdue(datetime(2000, 1, 2), datetime(2000, 1, 1)))
        