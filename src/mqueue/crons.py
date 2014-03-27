# -*- coding: utf-8 -*-
import doctest

MINUTELY = '* * * * *'
HOURLY = '0 * * * *'
DAILY = '0 0 * * *'
WEEKLY = '0 0 * * 0'
MONTHLY = '0 0 1 * *'

def MINUTES(interval):
    '''
    >>> MINUTES(5)
    '*/5 * * * *'
    '''
    return '*/%d * * * *' % interval

def HOURS(interval):
    '''
    >>> HOURS(4)
    '* */4 * * *'
    '''
    return '* */%d * * *' % interval

def DAYS(interval):
    '''
    >>> DAYS(3)
    '* * */3 * *'
    '''
    return '* * */%d * *' % interval

if __name__ == '__main__':
    doctest.testmod()
    