# -*- coding: utf-8 -*-
from mqueue.util import Timer
from testutil import TestCase
import time

class TimerTest(TestCase):
    def test_suceess(self):
        class TestTimer(Timer):
            interval = 0.01
            iterations = 0
            
            def _run(self):
                self.iterations += 1
        timer = TestTimer()
        timer.start()
        time.sleep(0.1)
        self.assertTrue(timer.is_alive())
        timer.stop()
        self.assertFalse(timer.is_alive())
        iterations = timer.iterations
        self.assertTrue(iterations >= 1 and iterations <= 20)
        
    def test_error(self):
        class TestTimer(Timer):
            error_delay = 0
            interval = 0.01
            iterations = 0
            
            def _run(self):
                self.iterations += 1
                raise Exception()
        timer = TestTimer()
        timer.start()
        time.sleep(0.1)
        self.assertTrue(timer.is_alive())
        timer.stop()
        iterations = timer.iterations
        self.assertTrue(iterations >= 1 and iterations <= 20)
        