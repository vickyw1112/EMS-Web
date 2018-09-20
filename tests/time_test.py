import pytest
from model.time import Time
from model.timeFormatter import DayFormatter, HourFormatter

def test_DayFormatter_duration():
    time1 = Time('2005-06-01T13:33', '2005-06-02T13:33', DayFormatter)
    assert(time1.duration == '1 Day')

def test_HourFormatter_duration():
    time1 = Time('2005-06-01T13:33', '2005-06-01T15:33', HourFormatter)
    assert(time1.duration == '2 Hours')

def test_HourFormatter_duration_involve_min():
    time1 = Time('2005-06-01T13:33', '2005-06-01T15:54', HourFormatter)
    assert(time1.duration == '2 Hours 21 Minutes')
    time1 = Time('2005-06-01T13:33', '2005-06-01T14:34', HourFormatter)
    assert(time1.duration == '1 Hour 1 Minute')

def test_DayFormatter_duration_days():
    time1 = Time('2005-06-01T13:33', '2005-06-07T13:33', DayFormatter)
    assert(time1.duration == '6 Days')


def test_DayFormatter_duration_days_roundup():
    time1 = Time('2005-06-01T13:33', '2005-06-07T13:34', DayFormatter)
    assert(time1.duration == '7 Days')

def test_HourFormatter_toStr_past_year():
    time1 = Time('2005-06-01T13:33',  '2005-06-01T14:34', HourFormatter)
    assert(str(time1) == '01/06/2005 13:33 to 14:34')
    
def test_HourFormatter_toStr_curr_year():
    time1 = Time('2018-06-01T13:33',  '2018-06-01T14:34', HourFormatter)
    assert(str(time1) == '01/06 13:33 to 14:34')

def test_DayFormatter_toStr_past_year():
    time1 = Time('2005-06-01T13:33', '2005-06-08T16:33', DayFormatter)
    assert(str(time1) == '01/06/2005 to 08/06/2005')

def test_DayFormatter_toStr_diff_year():
    time1 = Time('2018-06-01T13:33', '2019-02-01T13:03', DayFormatter)
    assert(str(time1) == '01/06/2018 to 01/02/2019')
   
def test_DayFormatter_toStr_curr_year():
    time1 = Time('2018-01-01T13:33', '2018-02-01T13:03', DayFormatter)
    assert(str(time1) == '01/01 to 01/02')


if __name__ == '__main__':
    pytest.main()
