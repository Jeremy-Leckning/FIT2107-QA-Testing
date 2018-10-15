'''A class to calculate optimal times for satellite spotting
Initial skeleton code written by Robert Merkel for FIT2107 Assignment 3
'''

from skyfield.api import Loader
from skyfield.api import Topos, load

#import pytz,datetime, time
from datetime import datetime, timedelta
from pytz import timezone
# import pytz,datetime, time



class IllegalArgumentException(Exception):
    '''An exception to throw if somebody provides invalid data to the Scheduler methods'''
    def __init__(self):
        pass

    def __str__(self):
        print("There is an error with the arguments")


class Scheduler:
    '''The class for calculating optimal satellite spotting times.  You can and should add methods
    to this, but please don't change the parameter list for the existing methods.  '''
    def __init__(self):
        '''Constructor sets things to put downloaded data in a sensible location. You can add
        to this if you want.  '''
        self._skyload = Loader('~/.skyfield-data')
        self.ts = self._skyload.timescale()
        self.t = 0

    def load_satellites(self, satlist_url='http://celestrak.com/NORAD/elements/visual.txt'):
        """
        loads the list of satellites from a given url into an array
        @return: list of satellite
        """
        satellites = load.tle(satlist_url)
        return satellites

    def find_time(self, satlist_url='http://celestrak.com/NORAD/elements/visual.txt',
    start_time=datetime.now(), n_windows=24, duration=60, sample_interval=1, cumulative=False,
    location=(-37.910496,145.134021)):
        '''NOTE: this is the key function that you'll need to implement for the assignment.  Please
        don't change the arguments.
        arguments: satlist_url (string) a URL to a file containing a list of Earth-orbiting
        satellites in TLE format)
                      start_time: a Python Datetime object representing the
                      the start of the potential observation windows,return

                      duration: the size (in minutes) of an observation window - must be positive
                      n_windows: the number of observation windows to check.  Must be a positive integer
                      sample_interval: the interval (in minutes) at which the visible
                      satellites are checked.  Must be smaller than duration.
                      cumulative: a boolean to determine whether we look for the maximum number
                      of satellites visible at any time within the duration (if False), or the
                      cumulative number of distinct satellites visible over the duration (if True)
                      location: a tuple (lat, lon) of floats specifying he latitude and longitude of the
                      observer.  Negative latitudes specify the southern hemisphere, negative longitudes
                      the western hemisphere.  lat must be in the range [-90,90], lon must be in the
                      range [-180, 180]
        returns:a tuple ( interval_start_time, satellite_list), where start_interval is
        the time interval from the set {(start_time, start_time + duration),
        (start_time + duration, start_time + 2*duration)...} with the most satellites visible at some
        point in the interval, or the most cumulative satellites visible over the interval (if cumulative=True)
        See the assignment spec sheet for more details.
        raises: IllegalArgumentException if an illegal argument is provided'''

        # Handling illegal arguments
        if type(start_time) is not type(datetime.now()):
            raise IllegalArgumentException()
        if duration <= 0:
            raise IllegalArgumentException()
        if not isinstance(n_windows, int) or n_windows < 0:
            raise IllegalArgumentException()
        if sample_interval >= duration:
            raise IllegalArgumentException()
        if not isinstance(cumulative, bool):
            raise IllegalArgumentException()
        if not isinstance(location, tuple):
            raise IllegalArgumentException()
        if location[0] < -90 or location[0] > 90:
            raise IllegalArgumentException()
        if location[1] < -180 or location[1] > 180:
            raise IllegalArgumentException()

        # Local variables
        satellite_list = []
        time_list = []
        count_list = []

        if cumulative == False:  # return(time_interval, list of satellites visible during window of time)

            for window in range(n_windows):
                self.t = start_time + timedelta(minutes=duration*window)
                #time_list.append(self.t)
                temp = self.max(satlist_url, self.t, duration, sample_interval, location)
                time_list.append(temp[0])
                count_list.append(temp[1])  # adding count only
                satellite_list.append(temp[2])
            max_value = max(count_list)
            max_index = count_list.index(max_value)
            max_time_value = time_list[max_index]
            max_satellite_list = satellite_list[max_index]
            #string = max_time_value.strftime("%H") + ":" + max_time_value.strftime("%M")
            return (max_time_value, max_satellite_list) #  return (string, max_value, max_satellite_list)

        elif cumulative == True:
            for window in range(n_windows):
                self.t = start_time + timedelta(minutes=duration*window)
                # time_list.append(self.t)
                temp = self.total(satlist_url, self.t, duration, sample_interval, location)
                time_list.append(temp[0])
                count_list.append(temp[1])  # adding count only
                satellite_list.append(temp[2]) # satellite_list holds arrays of satellites for each windows. Hence
                # satellite_list[0] returns the list of satellites for the first viewing window
            max_value = max(count_list)
            max_index = count_list.index(max_value)
            max_time_value = time_list[max_index]
            max_satellite_list = satellite_list[max_index]
            # string = max_time_value.strftime("%H") + ":" + max_time_value.strftime("%M")
            return (max_time_value, max_satellite_list)  # return (string, max_value, max_satellite_list)

        self.t = 0

    def max(self, satlist_url='http://celestrak.com/NORAD/elements/visual.txt',
    start_time=datetime.now(), duration=60, sample_interval=1, location=(-37.910496,145.134021)):
        """
        calculates the maximum number of satellites visible at a single moment within an interval of time
        @param satlist_url: the website where we get the list of satellites
        @param start_time: the time where we want to start measure the number of satellites visible
        @param duration: the duration during which we want to measure the number of satellites visible
        @sample_interval: the intervals of time during which we will measure the number of visible satellites
        @location: the user's location
        @return: a tuple (time interval, max_number_of_satellites, list of satellites)
        """

        # Loading list of satellites
        satellites = self.load_satellites(satlist_url)
        # Local variables used inside loop
        UTC_ZONE = timezone('UTC')
        current_max_list = []
        max_count = 0

        for j in range(0, duration, sample_interval):
            # Resetting local variables after each iteration
            satellite_list = []
            count = 0

            # Getting time we want to calculate
            self.t = start_time + timedelta(minutes = j)
            e = UTC_ZONE.localize(self.t)
            self.t = self.ts.utc(e)

            for i in satellites:
                if isinstance(i, str):
                    continue

                # Determining whether satellite is visible or not
                satellite = satellites[i]
                bluffton = Topos(location[0], location[1])
                difference = satellite - bluffton
                topocentric = difference.at(self.t)
                alt, az, distance = topocentric.altaz()

                if alt.degrees > 0:
                    satellite_list.append(satellite)
                    count += 1

            # keeping record of max number of satellites visible at any time within interval
            if count > max_count:
                current_max_list = satellite_list
                max_count = count
                peak_time = start_time + timedelta(minutes = j)
            timestring = start_time.strftime("%H") + ":" + start_time.strftime("%M")
        return (timestring, max_count, current_max_list)

    def total(self, satlist_url='http://celestrak.com/NORAD/elements/visual.txt',
    start_time=datetime.now(),duration=60, sample_interval=1,
    location=(-37.910496,145.134021)):
        """
        calculates the total number of distinct satellites for a given time interval
        @param satlist_url: the website where we get the list of satellites
        @param start_time: the time where we want to start measure the number of satellites visible
        @param duration: the duration during which we want to measure the number of satellites visible
        @sample_interval: the intervals of time during which we will measure the number of visible satellites
        @location: the user's location
        @return: a tuple (start_time, number of distinct satellites, list of distinct satellites)
        """

        # Loading list of satellites
        satellites = self.load_satellites(satlist_url)

        # Local variables used inside loop
        satellite_list = []
        UTC_ZONE = timezone('UTC')

        for j in range(0, duration, sample_interval):
            # Resetting local variables

            # Getting time we want to calculate
            self.t = start_time + timedelta(minutes=j)
            e = UTC_ZONE.localize(self.t)
            self.t = self.ts.utc(e)

            # Looping through satellites list
            for i in satellites:
                if isinstance(i, str):
                    continue

                # Determining whether satellite is visible or not
                satellite = satellites[i]
                bluffton = Topos(location[0], location[1])
                difference = satellite - bluffton
                topocentric = difference.at(self.t)

                alt, az, distance = topocentric.altaz()

                if alt.degrees > 0 and satellite not in satellite_list:
                    satellite_list.append(satellite)
        self.t = 0
        timestring = start_time.strftime("%H") + ":" + start_time.strftime("%M")
        return (timestring, len(satellite_list), satellite_list)
