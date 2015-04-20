# -*- coding: utf-8 -*-
from datetime import timedelta
from decorated.base.context import Context
from fixtures2 import TestCase
from mqueue.decorators import Delay

class DelayTest(TestCase):
    def test_with_delay(self):
        delay = timedelta(minutes=5)
        with Delay(delay):
            self.assertEqual(delay, Delay.value())
            
    def test_no_delay(self):
        with Context():
            self.assertEqual(timedelta(minutes=0), Delay.value())
            
    def test_no_context(self):
        self.assertEqual(timedelta(minutes=0), Delay.value())
