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
    >>> schedule = CronSchedule('0 * * * *')
    
    >>> str(schedule)
    'CronSchedule(0 * * * *)'
    
    >>> schedule.is_overdue(datetime(2000, 1, 1, 1, 0, 0), datetime(2000, 1, 1, 0, 0, 0))
    True
    >>> schedule.is_overdue(datetime(2000, 1, 1, 0, 30, 0), datetime(2000, 1, 1, 0, 0, 0))
    False
    '''
    
    def __init__(self, cron):
        super(CronSchedule, self).__init__()
        self._expression = cron
        self._cron = CronTab(cron)
        
    def __str__(self):
        return 'CronSchedule(%s)' % self._expression
        
    def is_overdue(self, now, last):
        delta = self._cron.next(last)
        delta = timedelta(seconds=delta)
        return last + delta <= now
    
class Minutely(CronSchedule):
    '''
    >>> from datetime import datetime
    >>> schedule = Minutely()
    >>> schedule.is_overdue(datetime(2000, 1, 1, 0, 1, 0), datetime(2000, 1, 1, 0, 0, 0))
    True
    >>> schedule.is_overdue(datetime(2000, 1, 1, 0, 0, 30), datetime(2000, 1, 1, 0, 0, 0))
    False
    '''
    
    def __init__(self):
        super(Minutely, self).__init__('* * * * *')
        
class Hourly(CronSchedule):
    '''
    >>> from datetime import datetime
    
    >>> schedule = Hourly()
    >>> schedule.is_overdue(datetime(2000, 1, 1, 1, 0, 0), datetime(2000, 1, 1, 0, 0, 0))
    True
    >>> schedule.is_overdue(datetime(2000, 1, 1, 0, 30, 0), datetime(2000, 1, 1, 0, 0, 0))
    False
    
    >>> schedule = Hourly(30)
    >>> schedule.is_overdue(datetime(2000, 1, 1, 1, 30, 0), datetime(2000, 1, 1, 0, 30, 0))
    True
    >>> schedule.is_overdue(datetime(2000, 1, 1, 1, 0, 0), datetime(2000, 1, 1, 0, 30, 0))
    False
    '''
    
    def __init__(self, minute=0):
        super(Hourly, self).__init__('%d * * * *' % minute)
        
class Daily(CronSchedule):
    '''
    >>> from datetime import datetime
    
    >>> schedule = Daily()
    >>> schedule.is_overdue(datetime(2000, 1, 2, 0, 0, 0), datetime(2000, 1, 1, 0, 0, 0))
    True
    >>> schedule.is_overdue(datetime(2000, 1, 1, 12, 0, 0), datetime(2000, 1, 1, 0, 0, 0))
    False
    
    >>> schedule = Daily(12)
    >>> schedule.is_overdue(datetime(2000, 1, 2, 12, 0, 0), datetime(2000, 1, 1, 12, 0, 0))
    True
    >>> schedule.is_overdue(datetime(2000, 1, 1, 1, 0, 0), datetime(2000, 1, 1, 12, 0, 0))
    False
    '''
    
    def __init__(self, hour=0):
        super(Daily, self).__init__('0 %d * * *' % hour)
        
class Weekly(CronSchedule):
    '''
    >>> from datetime import datetime
    
    >>> schedule = Weekly()
    >>> schedule.is_overdue(datetime(2000, 1, 10, 0, 0, 0), datetime(2000, 1, 3, 0, 0, 0))
    True
    >>> schedule.is_overdue(datetime(2000, 1, 6, 0, 0, 0), datetime(2000, 1, 3, 0, 0, 0))
    False
    
    >>> schedule = Weekly(3)
    >>> schedule.is_overdue(datetime(2000, 1, 13, 0, 0, 0), datetime(2000, 1, 6, 0, 0, 0))
    True
    >>> schedule.is_overdue(datetime(2000, 1, 10, 0, 0, 0), datetime(2000, 1, 6, 0, 0, 0))
    False
    '''
    
    def __init__(self, day=0):
        super(Weekly, self).__init__('0 0 * * %d' % day)
        
class Monthly(CronSchedule):
    '''
    >>> from datetime import datetime
    
    >>> schedule = Monthly()
    >>> schedule.is_overdue(datetime(2000, 2, 1, 0, 0, 0), datetime(2000, 1, 1, 0, 0, 0))
    True
    >>> schedule.is_overdue(datetime(2000, 1, 15, 0, 0, 0), datetime(2000, 1, 1, 0, 0, 0))
    False
    
    >>> schedule = Monthly(15)
    >>> schedule.is_overdue(datetime(2000, 2, 15, 0, 0, 0), datetime(2000, 1, 15, 0, 0, 0))
    True
    >>> schedule.is_overdue(datetime(2000, 2, 1, 0, 0, 0), datetime(2000, 1, 15, 0, 0, 0))
    False
    '''
    
    def __init__(self, day=1):
        super(Monthly, self).__init__('0 0 %d * *' % day)
        
class Yearly(CronSchedule):
    '''
    >>> from datetime import datetime
    
    >>> schedule = Yearly()
    >>> schedule.is_overdue(datetime(2001, 1, 1, 0, 0, 0), datetime(2000, 1, 1, 0, 0, 0))
    True
    >>> schedule.is_overdue(datetime(2000, 7, 1, 0, 0, 0), datetime(2000, 1, 1, 0, 0, 0))
    False
    
    >>> schedule = Yearly(7)
    >>> schedule.is_overdue(datetime(2001, 7, 1, 0, 0, 0), datetime(2000, 7, 1, 0, 0, 0))
    True
    >>> schedule.is_overdue(datetime(2001, 1, 1, 0, 0, 0), datetime(2000, 7, 1, 0, 0, 0))
    False
    '''
    
    def __init__(self, month=1):
        super(Yearly, self).__init__('0 0 1 %d *' % month)
        
class Minutes(CronSchedule):
    '''
    >>> from datetime import datetime
    >>> schedule = Minutes(5)
    >>> schedule.is_overdue(datetime(2000, 1, 1, 0, 5, 0), datetime(2000, 1, 1, 0, 0, 0))
    True
    >>> schedule.is_overdue(datetime(2000, 1, 1, 0, 3, 0), datetime(2000, 1, 1, 0, 0, 0))
    False
    '''
    
    def __init__(self, interval):
        super(Minutes, self).__init__('*/%d * * * *' % interval)
        
class Hours(CronSchedule):
    '''
    >>> from datetime import datetime
    >>> schedule = Hours(4)
    >>> schedule.is_overdue(datetime(2000, 1, 1, 4, 0, 0), datetime(2000, 1, 1, 0, 0, 0))
    True
    >>> schedule.is_overdue(datetime(2000, 1, 1, 3, 0, 0), datetime(2000, 1, 1, 0, 0, 0))
    False
    '''
    
    def __init__(self, interval):
        super(Hours, self).__init__('0 */%d * * *' % interval)

class Days(CronSchedule):
    '''
    >>> from datetime import datetime
    >>> schedule = Days(5)
    >>> schedule.is_overdue(datetime(2000, 1, 6, 0, 0, 0), datetime(2000, 1, 1, 0, 0, 0))
    True
    >>> schedule.is_overdue(datetime(2000, 1, 3, 0, 0, 0), datetime(2000, 1, 1, 0, 0, 0))
    False
    '''
    
    def __init__(self, interval):
        super(Days, self).__init__('0 0 */%d * *' % interval)
        
class Months(CronSchedule):
    '''
    >>> from datetime import datetime
    >>> schedule = Months(3)
    >>> schedule.is_overdue(datetime(2000, 4, 1, 0, 0, 0), datetime(2000, 1, 1, 0, 0, 0))
    True
    >>> schedule.is_overdue(datetime(2000, 3, 1, 0, 0, 0), datetime(2000, 1, 1, 0, 0, 0))
    False
    '''
    
    def __init__(self, interval):
        super(Months, self).__init__('0 0 1 */%d *' % interval)

if __name__ == '__main__':
    doctest.testmod()
    