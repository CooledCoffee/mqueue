# -*- coding: utf-8 -*-
from datetime import datetime
from fixtures2.mox import MoxFixture
from mqueue import scheduler
from mqueue.db import Cron as CronModel
from mqueue.decorators import Cron
from testutil import DbTest

@Cron('* * * * *')
def foo():
    pass

@Cron('* * * * *')
def bar():
    pass

class CheckAndRunTest(DbTest):
    def setUp(self):
        super(CheckAndRunTest, self).setUp()
        self.mox = self.useFixture(MoxFixture())
        self.mox.mock(foo, 'enqueue')
        
    def test_overdue(self):
        # set up
        with self.mysql.dao.create_session() as session:
            session.add(CronModel(queue='queue1', name='scheduler_test.foo', last=datetime(2000, 1, 1)))
            
        # test
        with self.mox.record():
            foo.enqueue()
        with self.mox.replay():
            scheduler._check_and_run(foo)
        
    def test_not_overdue(self):
        # set up
        with self.mysql.dao.create_session() as session:
            session.add(CronModel(queue='queue1', name='scheduler_test.foo', last=datetime(2050, 1, 1)))
            
        # test
        with self.mox.replay():
            scheduler._check_and_run(foo)
            
    def test_first_time(self):
        with self.mox.record():
            foo.enqueue()
        with self.mox.replay():
            scheduler._check_and_run(foo)
            