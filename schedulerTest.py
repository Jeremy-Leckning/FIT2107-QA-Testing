import unittest
from scheduler import Scheduler
from scheduler import IllegalArgumentException
from datetime import datetime
from unittest.mock import patch, MagicMock


class SchedulerTest(unittest.TestCase):
    '''Tests for the scheduler class.  Add more tests
    to test the code that you write'''

    def setUp(self):
        self.scheduler = Scheduler()

    def test_findTime(self):
        (timeInterval, totalNumberOfSatellites) = self.scheduler.find_time(satlist_url='http://celestrak.com/NORAD/elements/visual.txt',
    start_time=datetime.now(), n_windows=2, duration=60, sample_interval=1, cumulative=True,
    location=(-37.910496,145.134021))

        self.assertTrue(type(totalNumberOfSatellites) == int)
        self.assertTrue(totalNumberOfSatellites>0)

        (timeInterval, maxNumberOfSatellites) = self.scheduler.find_time(satlist_url='http://celestrak.com/NORAD/elements/visual.txt',
    start_time=datetime.now(), n_windows=2, duration=60, sample_interval=1, cumulative=False,
    location=(-37.910496,145.134021))
        self.assertTrue(isinstance(maxNumberOfSatellites, int))

    def test_max(self):
        (startTime, maximumNumber) = self.scheduler.max(satlist_url='http://celestrak.com/NORAD/elements/visual.txt', start_time=datetime.now(), duration=60, sample_interval=1, location=(-37.910496,145.134021))
        self.assertTrue(type(maximumNumber) == int)
        self.assertTrue(maximumNumber >= 0)

    def test_total(self):
        totalNumberOfSatellites = self.scheduler.total(satlist_url='http://celestrak.com/NORAD/elements/visual.txt',
    start_time=datetime.now(),duration=60, sample_interval=1,
    location=(-37.910496,145.134021))
        self.assertTrue(type(totalNumberOfSatellites) == int)
        self.assertTrue(totalNumberOfSatellites >= 0)


    def test_exceptionthrown(self):
        with self.assertRaises(IllegalArgumentException):
            (stime, satellites) = self.scheduler.find_time(start_time = "now")
        with self.assertRaises(IllegalArgumentException):
            (stime, satellites) = self.scheduler.find_time(n_windows = -5)
        with self.assertRaises(IllegalArgumentException):
            (stime, satellites) = self.scheduler.find_time(n_windows = "a")
        with self.assertRaises(IllegalArgumentException):
            (stime, satellites) = self.scheduler.find_time(duration = 15, sample_interval=20)
        with self.assertRaises(IllegalArgumentException):
            (stime, satellites) = self.scheduler.find_time(location = (-100,200))
        with self.assertRaises(IllegalArgumentException):
            (stime, satellites) = self.scheduler.find_time(cumulative = "hello")


"""
    def test_itsalive(self):
        (stime, satellites) = self.scheduler.find_time()
        self.assertTrue(type(stime)==type(datetime.now()))
        self.assertTrue(satellites[0]=="ISS (ZARYA)")
        self.assertTrue(satellites[1]=="COSMOS-123")
"""

if __name__=="__main__":
    unittest.main()
