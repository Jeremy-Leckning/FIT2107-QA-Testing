import unittest
from scheduler import Scheduler
from scheduler import IllegalArgumentException
from datetime import datetime
from unittest.mock import patch, MagicMock, create_autospec


class SchedulerTest(unittest.TestCase):
    '''Tests for the scheduler class.  Add more tests
    to test the code that you write'''

    def setUp(self):
        self.scheduler = Scheduler()


    def test_findTime(self):
        realScheduler = Scheduler()
        realScheduler.max = MagicMock()
        realScheduler.max.side_effect = [("00:00", 4, ["sat1", "sat2", "sat3", "sat4"]),("00:00", 2, ["sat1", "sat2"]),("01:00",5,["sat1", "sat2", "sat3", "sat4", "sat5"])]
        self.assertTrue(realScheduler.max.call_count == 0)
        (timeInterval, listOfSatellites) = realScheduler.find_time(satlist_url='http://celestrak.com/NORAD/elements/visual.txt',
    start_time=datetime.now(), n_windows=3, duration=60, sample_interval=1, cumulative=False, location=(-37.910496,145.134021))
        print(timeInterval)
        print(listOfSatellites)
        self.assertTrue(listOfSatellites == ["sat1","sat2","sat3","sat4","sat5"])
        self.assertTrue(len(listOfSatellites)>=0)
        self.assertTrue(realScheduler.max.call_count == 3)


        (timeInterval, listOfSatellites) = self.scheduler.find_time(satlist_url='http://celestrak.com/NORAD/elements/visual.txt',
    start_time=datetime.now(), n_windows=2, duration=60, sample_interval=1, cumulative=False,
    location=(-37.910496,145.134021))




    def test_total(self):
        totalNumberOfSatellites = self.scheduler.total(satlist_url='http://celestrak.com/NORAD/elements/visual.txt',
    start_time=datetime.now(),duration=60, sample_interval=1,
    location=(-37.910496,145.134021))
        self.assertTrue(type(totalNumberOfSatellites) == int)
        self.assertTrue(totalNumberOfSatellites >= 0)

    def test_load_satellites(self):
        """
        tests load satellites using Mocking
        """
        realScheduler = Scheduler()
        schedulerMock = create_autospec(realScheduler)
        schedulerMock.load_satellites.return_value = ["sat1", "sat2", "sat3", "sat4"]
        satellites = schedulerMock.load_satellites()
        self.assertTrue(satellites == ["sat1", "sat2", "sat3", "sat4"])
        schedulerMock.load_satellites.assert_called_once() # assert that is has been called only once
        schedulerMock.load_satellites.assert_called_with() # called with no arguments

    # def test_max(self):
    #     realScheduler = Scheduler()
    #     # listOfSat = {694: <EarthSatellite 'ATLAS CENTAUR 2' number=694 epoch=2018-10-08T17:08:05Z>}
    #
    #     # realScheduler.load_satellites = MagicMock(return_value = listOfSat)
    #     # schedulerMock = MagicMock()
    #     # schedulerMock = create_autospec(realScheduler)
    #
    #     (startTime, maximumNumber, satellites) = realScheduler.max(satlist_url='http://celestrak.com/NORAD/elements/visual.txt', start_time=datetime(2018, 10, 8, 0, 0, 0, 0), duration=60, sample_interval=4, location=(-37.910496,145.134021))
    #     self.assertTrue(type(maximumNumber) == int)
    #     self.assertTrue(maximumNumber >= 0)
    #     print(maximumNumber)
    #     self.assertTrue(maximumNumber == 1)


    def test_exceptionthrown(self):
        with self.assertRaises(IllegalArgumentException):
            (stime, satellites) = self.scheduler.find_time(start_time="now")
        with self.assertRaises(IllegalArgumentException):
            (stime, satellites) = self.scheduler.find_time(n_windows=-5)
        with self.assertRaises(IllegalArgumentException):
            (stime, satellites) = self.scheduler.find_time(n_windows="a")
        with self.assertRaises(IllegalArgumentException):
            (stime, satellites) = self.scheduler.find_time(duration=15, sample_interval=20)
        with self.assertRaises(IllegalArgumentException):
            (stime, satellites) = self.scheduler.find_time(location=(-100,200))
        with self.assertRaises(IllegalArgumentException):
            (stime, satellites) = self.scheduler.find_time(cumulative="hello")

"""
    def test_itsalive(self):
        (stime, satellites) = self.scheduler.find_time()
        self.assertTrue(type(stime)==type(datetime.now()))
        self.assertTrue(satellites[0]=="ISS (ZARYA)")
        self.assertTrue(satellites[1]=="COSMOS-123")
"""


if __name__ == "__main__":
    unittest.main()
