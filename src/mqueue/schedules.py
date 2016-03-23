# -*- coding: utf-8 -*-
from crontab._crontab import CronTab
from datetime import timedelta
import doctest

class Schedule(object):
    def __init__(self):
        self.interval = None
    
    def is_overdue(self, now, last):
        raise NotImplementedError()
    
class CronSchedule(Schedule):
    '''
    >>> from datetime import datetime
    >>> schedule = CronSchedule('0 * * * *')
    
    >>> str(schedule)
    '0 * * * *'
    
    >>> schedule.is_overdue(datetime(2000, 1, 1, 1, 0, 0), datetime(2000, 1, 1, 0, 0, 0))
    True
    >>> schedule.is_overdue(datetime(2000, 1, 1, 0, 30, 0), datetime(2000, 1, 1, 0, 0, 0))
    False
    '''
    
    def __init__(self, expression):
        super(CronSchedule, self).__init__()
        self._expression = expression
        self._cron = CronTab(expression)
        
    def __str__(self):
        return self._expression
        
    def is_overdue(self, now, last):
        delta = self._cron.next(last)
        delta = timedelta(seconds=delta)
        return last + delta <= now
    
class Minutely(CronSchedule):
    '''
    >>> Minutely()._expression
    '* * * * *'
    '''
    
    def __init__(self):
        super(Minutely, self).__init__('* * * * *')
        self.interval = 60
        
class Hourly(CronSchedule):
    '''
    >>> Hourly()._expression
    '0 * * * *'
    >>> Hourly(30)._expression
    '30 * * * *'
    '''
    
    def __init__(self, minute=0):
        super(Hourly, self).__init__('%d * * * *' % minute)
        self.interval = 3600
        
class Daily(CronSchedule):
    '''
    >>> Daily()._expression
    '0 0 * * *'
    >>> Daily(12)._expression
    '0 12 * * *'
    '''
    
    def __init__(self, hour=0):
        super(Daily, self).__init__('0 %d * * *' % hour)
        self.interval = 86400
        
class Weekly(CronSchedule):
    '''
    >>> Weekly()._expression
    '0 0 * * 0'
    >>> Weekly(3)._expression
    '0 0 * * 3'
    '''
    
    def __init__(self, day=0):
        super(Weekly, self).__init__('0 0 * * %d' % day)
        self.interval = 86400 * 7
        
class Monthly(CronSchedule):
    '''
    >>> Monthly()._expression
    '0 0 1 * *'
    >>> Monthly(15)._expression
    '0 0 15 * *'
    '''
    
    def __init__(self, day=1):
        super(Monthly, self).__init__('0 0 %d * *' % day)
        
class Yearly(CronSchedule):
    '''
    >>> Yearly()._expression
    '0 0 1 1 *'
    >>> Yearly(7)._expression
    '0 0 1 7 *'
    '''
    
    def __init__(self, month=1):
        super(Yearly, self).__init__('0 0 1 %d *' % month)
        
class Minutes(CronSchedule):
    '''
    >>> Minutes(5)._expression
    '*/5 * * * *'
    '''
    
    def __init__(self, interval):
        super(Minutes, self).__init__('*/%d * * * *' % interval)
        self.interval = 60 * interval
        
class Hours(CronSchedule):
    '''
    >>> Hours(3)._expression
    '0 */3 * * *'
    '''
    
    def __init__(self, interval):
        super(Hours, self).__init__('0 */%d * * *' % interval)
        self.interval = 3600 * interval

class Days(CronSchedule):
    '''
    >>> Days(5)._expression
    '0 0 */5 * *'
    '''
    
    def __init__(self, interval):
        super(Days, self).__init__('0 0 */%d * *' % interval)
        self.interval = 86400 * interval
        
class Months(CronSchedule):
    '''
    >>> Months(3)._expression
    '0 0 1 */3 *'
    '''
    
    def __init__(self, interval):
        super(Months, self).__init__('0 0 1 */%d *' % interval)

class Weekday(CronSchedule):
    '''
    >>> Weekday()._expression
    '0 0 * * 1-5'
    >>> Weekday(12)._expression
    '0 12 * * 1-5'
    '''
    
    def __init__(self, hour=0):
        super(Weekday, self).__init__('0 %d * * 1-5' % hour)
        
if __name__ == '__main__':
    doctest.testmod()
    