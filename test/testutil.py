# -*- coding: utf-8 -*-
from fixtures2.case import TestCase
from fixtures2.patches import PatchesFixture
from sqlalchemy_dao.testing import MysqlFixture
import os

class TestCase(TestCase):
    def setUp(self):
        super(TestCase, self).setUp()
        self.patches = self.useFixture(PatchesFixture())
        
class DbTestCase(TestCase):
    def setUp(self):
        super(DbTestCase, self).setUp()
        self.patches.patch('mqueue.QUEUE', 'queue1')
        path = os.path.join(os.path.dirname(__file__), 'queue.sql')
        fixture = MysqlFixture(host='test', scripts=path, daos=['mqueue.db.dao'])
        self.mysql = self.useFixture(fixture)
        