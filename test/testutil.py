# -*- coding: utf-8 -*-
from datetime import datetime
from fixtures2.case import TestCase
from fixtures2.patches import PatchesFixture
from sqlalchemy_dao.testing import MysqlFixture
import os

class TestCase(TestCase):
    def setUp(self):
        super(TestCase, self).setUp()
        self.patches = self.useFixture(PatchesFixture())
        
class DbTest(TestCase):
    def assertAlmostNow(self, time):
        delta = abs(datetime.now() - time)
        if delta.seconds > 10:
            msg = '"%s" is not almost now' % (time.strftime('%Y-%m-%d %H:%M:%S'))
            raise self.failureException(msg)
            
    def setUp(self):
        super(DbTest, self).setUp()
        self.patches.patch('mqueue.QUEUE', 'queue1')
        path = os.path.join(os.path.dirname(__file__), 'queue.sql')
        self.mysql = self.useFixture(MysqlFixture([path], daos=['mqueue.db.dao']))
        