# -*- coding: utf-8 -*-
from crontab._crontab import CronTab
from datetime import timedelta
import doctest

class Schedule(object):
    def is_overdue(self, now, last):
        raise NotImplementedError()
    
class CronSchedule(Schedule):
    '''
    >>> from datetime import datetime
    >>> schedule = CronSchedule('*/5 * * * *')
    >>> schedule.is_overdue(datetime(2000, 1, 1, 0, 6, 0), datetime(2000, 1, 1, 0, 0, 0))
    True
    >>> schedule.is_overdue(datetime(2000, 1, 1, 0, 3, 0), datetime(2000, 1, 1, 0, 0, 0))
    False
    '''
    
    def __init__(self, cron):
        super(CronSchedule, self).__init__()
        self._cron = CronTab(cron)
        
    def is_overdue(self, now, last):
        delta = self._cron.next(last)
        delta = timedelta(seconds=delta)
        return last + delta <= now
    
class MINUTELY(CronSchedule):
    '''
    >>> from datetime import datetime
    >>> schedule = MINUTELY()
    >>> schedule.is_overdue(datetime(2000, 1, 1, 0, 1, 0), datetime(2000, 1, 1, 0, 0, 0))
    True
    >>> schedule.is_overdue(datetime(2000, 1, 1, 0, 0, 30), datetime(2000, 1, 1, 0, 0, 0))
    False
    '''
    
    def __init__(self):
        super(MINUTELY, self).__init__('* * * * *')
        
class HOURLY(CronSchedule):
    '''
    >>> from datetime import datetime
    
    >>> schedule = HOURLY()
    >>> schedule.is_overdue(datetime(2000, 1, 1, 1, 0, 0), datetime(2000, 1, 1, 0, 0, 0))
    True
    >>> schedule.is_overdue(datetime(2000, 1, 1, 0, 30, 0), datetime(2000, 1, 1, 0, 0, 0))
    False
    
    >>> schedule = HOURLY(30)
    >>> schedule.is_overdue(datetime(2000, 1, 1, 1, 30, 0), datetime(2000, 1, 1, 0, 30, 0))
    True
    >>> schedule.is_overdue(datetime(2000, 1, 1, 1, 0, 0), datetime(2000, 1, 1, 0, 30, 0))
    False
    '''
    
    def __init__(self, minute=0):
        super(HOURLY, self).__init__('%d * * * *' % minute)
        
class DAILY(CronSchedule):
    '''
    >>> from datetime import datetime
    
    >>> schedule = DAILY()
    >>> schedule.is_overdue(datetime(2000, 1, 2, 0, 0, 0), datetime(2000, 1, 1, 0, 0, 0))
    True
    >>> schedule.is_overdue(datetime(2000, 1, 1, 12, 0, 0), datetime(2000, 1, 1, 0, 0, 0))
    False
    
    >>> schedule = DAILY(12)
    >>> schedule.is_overdue(datetime(2000, 1, 2, 12, 0, 0), datetime(2000, 1, 1, 12, 0, 0))
    True
    >>> schedule.is_overdue(datetime(2000, 1, 1, 1, 0, 0), datetime(2000, 1, 1, 12, 0, 0))
    False
    '''
    
    def __init__(self, hour=0):
        super(DAILY, self).__init__('0 %d * * *' % hour)
        
class WEEKLY(CronSchedule):
    '''
    >>> from datetime import datetime
    
    >>> schedule = WEEKLY()
    >>> schedule.is_overdue(datetime(2000, 1, 10, 0, 0, 0), datetime(2000, 1, 3, 0, 0, 0))
    True
    >>> schedule.is_overdue(datetime(2000, 1, 6, 0, 0, 0), datetime(2000, 1, 3, 0, 0, 0))
    False
    
    >>> schedule = WEEKLY(3)
    >>> schedule.is_overdue(datetime(2000, 1, 13, 0, 0, 0), datetime(2000, 1, 6, 0, 0, 0))
    True
    >>> schedule.is_overdue(datetime(2000, 1, 10, 0, 0, 0), datetime(2000, 1, 6, 0, 0, 0))
    False
    '''
    
    def __init__(self, day=0):
        super(WEEKLY, self).__init__('0 0 * * %d' % day)
        
class MONTHLY(CronSchedule):
    '''
    >>> from datetime import datetime
    
    >>> schedule = MONTHLY()
    >>> schedule.is_overdue(datetime(2000, 2, 1, 0, 0, 0), datetime(2000, 1, 1, 0, 0, 0))
    True
    >>> schedule.is_overdue(datetime(2000, 1, 15, 0, 0, 0), datetime(2000, 1, 1, 0, 0, 0))
    False
    
    >>> schedule = MONTHLY(15)
    >>> schedule.is_overdue(datetime(2000, 2, 15, 0, 0, 0), datetime(2000, 1, 15, 0, 0, 0))
    True
    >>> schedule.is_overdue(datetime(2000, 2, 1, 0, 0, 0), datetime(2000, 1, 15, 0, 0, 0))
    False
    '''
    
    def __init__(self, day=1):
        super(MONTHLY, self).__init__('0 0 %d * *' % day)
        
class YEARLY(CronSchedule):
    '''
    >>> from datetime import datetime
    
    >>> schedule = YEARLY()
    >>> schedule.is_overdue(datetime(2001, 1, 1, 0, 0, 0), datetime(2000, 1, 1, 0, 0, 0))
    True
    >>> schedule.is_overdue(datetime(2000, 7, 1, 0, 0, 0), datetime(2000, 1, 1, 0, 0, 0))
    False
    
    >>> schedule = YEARLY(7)
    >>> schedule.is_overdue(datetime(2001, 7, 1, 0, 0, 0), datetime(2000, 7, 1, 0, 0, 0))
    True
    >>> schedule.is_overdue(datetime(2001, 1, 1, 0, 0, 0), datetime(2000, 7, 1, 0, 0, 0))
    False
    '''
    
    def __init__(self, month=1):
        super(YEARLY, self).__init__('0 0 1 %d *' % month)
        
class MINUTES(CronSchedule):
    '''
    >>> from datetime import datetime
    >>> schedule = MINUTES(5)
    >>> schedule.is_overdue(datetime(2000, 1, 1, 0, 5, 0), datetime(2000, 1, 1, 0, 0, 0))
    True
    >>> schedule.is_overdue(datetime(2000, 1, 1, 0, 3, 0), datetime(2000, 1, 1, 0, 0, 0))
    False
    '''
    
    def __init__(self, interval):
        super(MINUTES, self).__init__('*/%d * * * *' % interval)
        
class HOURS(CronSchedule):
    '''
    >>> from datetime import datetime
    >>> schedule = HOURS(4)
    >>> schedule.is_overdue(datetime(2000, 1, 1, 4, 0, 0), datetime(2000, 1, 1, 0, 0, 0))
    True
    >>> schedule.is_overdue(datetime(2000, 1, 1, 3, 0, 0), datetime(2000, 1, 1, 0, 0, 0))
    False
    '''
    
    def __init__(self, interval):
        super(HOURS, self).__init__('0 */%d * * *' % interval)

class DAYS(CronSchedule):
    '''
    >>> from datetime import datetime
    >>> schedule = DAYS(5)
    >>> schedule.is_overdue(datetime(2000, 1, 6, 0, 0, 0), datetime(2000, 1, 1, 0, 0, 0))
    True
    >>> schedule.is_overdue(datetime(2000, 1, 3, 0, 0, 0), datetime(2000, 1, 1, 0, 0, 0))
    False
    '''
    
    def __init__(self, interval):
        super(DAYS, self).__init__('0 0 */%d * *' % interval)
        
class MONTHS(CronSchedule):
    '''
    >>> from datetime import datetime
    >>> schedule = MONTHS(3)
    >>> schedule.is_overdue(datetime(2000, 4, 1, 0, 0, 0), datetime(2000, 1, 1, 0, 0, 0))
    True
    >>> schedule.is_overdue(datetime(2000, 3, 1, 0, 0, 0), datetime(2000, 1, 1, 0, 0, 0))
    False
    '''
    
    def __init__(self, interval):
        super(MONTHS, self).__init__('0 0 1 */%d *' % interval)

if __name__ == '__main__':
    doctest.testmod()
    