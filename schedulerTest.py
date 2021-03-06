import unittest
from scheduler import Scheduler
from scheduler import IllegalArgumentException
from datetime import datetime
from unittest.mock import patch, MagicMock, create_autospec

class SchedulerTest(unittest.TestCase):
    """Tests for the scheduler class.  Add more tests
    to test the code that you write"""
    def setUp(self):
        """
        the setUp method is run before the start of every test_ method
        """
        self.scheduler = Scheduler()

    def test_max(self):
        """
        Tests functionality of max() function using mocking
        return data values of load_satellites() and satellite_visibility function were mocked
        @raises: AssertionError if any of the tests fails
        """
        realScheduler = Scheduler()
        realScheduler.load_satellites= MagicMock(return_value={0: "sat1", 1:"sat2", 2:"sat3"})
        realScheduler.satellite_visibility = MagicMock()
        realScheduler.satellite_visibility.side_effect = 60*[True, False, True]
        (timestring, max_count, current_max_list) = realScheduler.max()
        self.assertTrue(type(max_count) == int)
        self.assertTrue(type(timestring) == str)
        self.assertTrue(len(current_max_list) == max_count)
        self.assertTrue(max_count == 2)
        self.assertTrue(current_max_list == ["sat1", "sat3"])


    def test_total(self):
        """
        Tests functionality of total() function using mocking
        return data values of load_satellites() and satellite_visibility function were mocked
        @raises: AssertionError if any of the tests fails
        """
        realScheduler = Scheduler()
        realScheduler.load_satellites = MagicMock(return_value={0: "sat1", 1: "sat2", 2: "sat3", 3:"sat4", 4:"sat5"})
        realScheduler.satellite_visibility = MagicMock()
        realScheduler.satellite_visibility.side_effect = 60 * [True, False, True, True, False]
        (timestring, max_count, current_max_list) = realScheduler.total()
        self.assertTrue(type(max_count) == int)
        self.assertTrue(type(timestring) == str)
        self.assertTrue(len(current_max_list) == max_count)
        self.assertTrue(max_count == 3)
        self.assertTrue(current_max_list == ["sat1", "sat3", "sat4"])

    def test_findTime_cumulative_false(self):
        """
        Tests functionality of find_time when cumulative = False, using mocking
        the return data value of max() method was mocked to test findtime method
        @raises: AssertionError if any of the tests fails
        """
        realScheduler = Scheduler()
        realScheduler.max = MagicMock()
        realScheduler.max.side_effect = [("00:00", 4, ["sat1", "sat2", "sat3", "sat4"]),("00:00", 2, ["sat1", "sat2"]),
                                         ("01:00", 5, ["sat1", "sat2", "sat3", "sat4", "sat5"])]
        self.assertTrue(realScheduler.max.call_count == 0)
        (timeInterval, listOfSatellites) = realScheduler.find_time(satlist_url='http://celestrak.com/NORAD/elements/visual.txt',
start_time=datetime.now(), n_windows=3, duration=60, sample_interval=1, cumulative=False, location=(-37.910496,145.134021))
        self.assertTrue(timeInterval == "01:00")
        self.assertTrue(listOfSatellites == ["sat1","sat2","sat3","sat4","sat5"])
        self.assertTrue(realScheduler.max.call_count == 3)

    def test_findTime_cumulative_true(self):
        """
        Tests functionality of find_time when cumulative = True, using mocking
        the return data value of max() method was mocked to test findtime method
        @raises: AssertionError if any of the tests fails
        """
        realScheduler = Scheduler()
        realScheduler.total = MagicMock()
        realScheduler.total.side_effect = [("00:00", 4, ["sat1", "sat6", "sat3", "sat4"]), ("01:00", 2, ["sat1", "sat7"]),
                                           ("02:00", 8, ["sat8", "sat9", "sat10", "sat4", "sat5, sat11, sat2, sat3"]),
                                           ("03:00", 5, ["sat1", "sat2", "sat3", "sat4", "sat5"])]
        self.assertTrue(realScheduler.total.call_count == 0)
        (timeInterval, listOfSatellites) = realScheduler.find_time(
            satlist_url='http://celestrak.com/NORAD/elements/visual.txt',
            start_time=datetime.now(), n_windows=4, duration=60, sample_interval=1, cumulative=True,
            location=(-37.910496, 145.134021))
        self.assertTrue(timeInterval == "02:00")
        self.assertTrue(listOfSatellites == ["sat8", "sat9", "sat10", "sat4", "sat5, sat11, sat2, sat3"])
        self.assertTrue(realScheduler.total.call_count == 4)

    def test_load_satellites(self):
        """
        tests load satellites using Mocking
        testing that load_satellites() function is being called correctly
        @raises: AssertionError if any of the tests fails
        """
        schedulerMock = create_autospec(self.scheduler)
        schedulerMock.load_satellites.return_value = ["sat1", "sat2", "sat3", "sat4"]
        satellites = schedulerMock.load_satellites()
        self.assertTrue(satellites == ["sat1", "sat2", "sat3", "sat4"])
        schedulerMock.load_satellites.assert_called_once()  # assert that is has been called only once
        schedulerMock.load_satellites.assert_called_with()  # called with no arguments

    def test_exceptionthrown(self):
        """
        tests whether IllegalArgumentExceptions are thrown when an illegal argument is used in the find_time function
        these tests are used to check whether an IllegalArgumentException is thrown every time an invalid argument
        is used for the findtime method.
        @raises: AssertionError if any of the tests fails
        """
        with self.assertRaises(IllegalArgumentException):
            (stime, satellites) = self.scheduler.find_time(start_time="now")
        with self.assertRaises(IllegalArgumentException):
            (stime, satellites) = self.scheduler.find_time(duration=-5)
        with self.assertRaises(IllegalArgumentException):
            (stime, satellites) = self.scheduler.find_time(n_windows=-5)
        with self.assertRaises(IllegalArgumentException):
            (stime, satellites) = self.scheduler.find_time(n_windows="a")
        with self.assertRaises(IllegalArgumentException):
            (stime, satellites) = self.scheduler.find_time(duration=15, sample_interval=20)
        with self.assertRaises(IllegalArgumentException):
            (stime, satellites) = self.scheduler.find_time(location=(-100,100))
        with self.assertRaises(IllegalArgumentException):
            (stime, satellites) = self.scheduler.find_time(location= [10, 10])
        with self.assertRaises(IllegalArgumentException):
            (stime, satellites) = self.scheduler.find_time(location=(10,200))
        with self.assertRaises(IllegalArgumentException):
            (stime, satellites) = self.scheduler.find_time(cumulative="hello")


if __name__ == "__main__":
    unittest.main()
