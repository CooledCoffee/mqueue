# -*- coding: utf-8 -*-
from datetime import datetime
from mqueue import decorators
from mqueue.decorators import Cron
from testutil import TestCase

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
        
class IsOverdueTest(TestCase):
    def test(self):
        @Cron('*/5 * * * *')
        def foo():
            pass
        self.assertTrue(foo.is_overdue(datetime(2000, 1, 1)))
        self.assertFalse(foo.is_overdue(datetime(2050, 1, 1)))
        