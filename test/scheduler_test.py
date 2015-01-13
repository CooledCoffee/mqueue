# -*- coding: utf-8 -*-
from datetime import datetime
from decorated.base.dict import Dict
from fixtures2 import DateTimeFixture
from fixtures2.mox import MoxFixture
from mqueue import scheduler
from mqueue.db import Cron as CronModel
from mqueue.decorators import Cron
from mqueue.scheduler import SchedulerThread
from testutil import DbTestCase, TestCase

@Cron('* * * * *')
def foo():
    pass

@Cron('* * * * *')
def bar():
    pass

class CheckTest(DbTestCase):
    def setUp(self):
        super(CheckTest, self).setUp()
        self.mox = self.useFixture(MoxFixture())
        self.mox.mock('scheduler_test.foo.enqueue')
        
    def test_overdue(self):
        # set up
        with self.mysql.dao.create_session() as session:
            session.add(CronModel(queue='queue1', name='scheduler_test.foo', last=datetime(2000, 1, 1)))
            
        # test
        with self.mox.record():
            foo.enqueue()
        with self.mox.replay():
            scheduler._check(foo, datetime(2000, 1, 2))
        with self.mysql.dao.create_session() as session:
            model = session.get(CronModel, 'queue1', 'scheduler_test.foo')
            self.assertEqual(datetime(2000, 1, 2), model.last)
        
    def test_not_overdue(self):
        # set up
        with self.mysql.dao.create_session() as session:
            session.add(CronModel(queue='queue1', name='scheduler_test.foo', last=datetime(2000, 1, 1)))
            
        # test
        with self.mox.replay():
            scheduler._check(foo, datetime(2000, 1, 1, 0, 0, 10))
        with self.mysql.dao.create_session() as session:
            model = session.get(CronModel, 'queue1', 'scheduler_test.foo')
            self.assertEqual(datetime(2000, 1, 1), model.last)
            
    def test_first_time(self):
        with self.mox.record():
            foo.enqueue()
        with self.mox.replay():
            scheduler._check(foo, datetime(2000, 1, 1))
        with self.mysql.dao.create_session() as session:
            model = session.get(CronModel, 'queue1', 'scheduler_test.foo')
            self.assertEqual(datetime(2000, 1, 1), model.last)
            
class IntervalTest(TestCase):
    def test(self):
        self.useFixture(DateTimeFixture('mqueue.scheduler.datetime', datetime(2000, 1, 1, 0, 0, 10)))
        scheduler = SchedulerThread()
        self.assertEqual(51, scheduler.interval)

class InitTest(DbTestCase):
    def test(self):
        # set up
        self.patches.patch('mqueue.QUEUE', 'queue1')
        crons = [
            Dict(name='tasks.cron1'),
            Dict(name='tasks.cron2'),
            Dict(name='tasks.cron3'),
        ]
        self.patches.patch('mqueue.decorators.crons', crons)
        with self.mysql.dao.create_session() as session:
            session.add(CronModel(queue='queue1', name='tasks.cron1', last='2000-01-01'))
            session.add(CronModel(queue='queue1', name='tasks.cron2', last='2000-01-01'))
            session.add(CronModel(queue='queue1', name='tasks.cron4', last='2000-01-01'))
            session.add(CronModel(queue='queue2', name='tasks.cron5', last='2000-01-01'))
            
        # test
        scheduler = SchedulerThread()
        scheduler._init()
        with self.mysql.dao.create_session() as session:
            self.assertEqual(3, session.query(CronModel).count())
