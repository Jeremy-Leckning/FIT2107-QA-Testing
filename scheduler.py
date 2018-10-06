'''A class to calculate optimal times for satellite spotting
Initial skeleton code written by Robert Merkel for FIT2107 Assignment 3
'''

from skyfield.api import Loader
from skyfield.api import Topos, load
import pytz,datetime, time
from datetime import datetime


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


        print(start_time)
        #Loading list of satellites
        satellites = load.tle(satlist_url)

        #Getting current time
        self.t = self.ts.now()
        print(self.t.utc_jpl())

        #Iterating over list of satellites to determine if they are over or below the horizon
        for i in satellites:
            if isinstance(i, str):
                continue


            print(i)

            satellite = satellites[i]
            bluffton = Topos(location[0], location[1])
            difference = satellite - bluffton
            topocentric = difference.at(self.t)

            alt, az, distance = topocentric.altaz()

            resultString=""
            resultString = str(satellites[i])
            if alt.degrees > 0:
                resultString+=" is above the horizon"
                print(resultString)
            else:
                resultString+=" is not above the horizon"
                print(resultString)
            # print(alt)
            # print(az)
            # print(distance.km)

        return (start_time, ["ISS (ZARYA)", "COSMOS-123"])
