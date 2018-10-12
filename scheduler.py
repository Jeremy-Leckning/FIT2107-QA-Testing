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

    def prompt(self):
        n_windows = input("?")
        duration = input("?")
        sampleInterval = input("?")
        cumulative = input("?")
        return (n_windows, duration, sampleInterval, cumulative)

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

        maxCountList = []
        Result = []
        stringList = []
        if cumulative == False:
            for window in range(n_windows):
                self.t = start_time + timedelta(minutes=duration*window)
                next_time = start_time + timedelta(minutes = duration * (window+1))
                Result.append((self.t, next_time))
                temp = self.max(satlist_url, self.t, duration, sample_interval, location)
                maxCountList.append(temp[1])  # adding count only
            max_value = max(maxCountList)
            max_index = maxCountList.index(max_value)
            max_time_value = Result[max_index]
            string = ""
            string = string + max_time_value[0].strftime("%H") + ":" + max_time_value[0].strftime("%M") + "," + max_time_value[1].strftime("%H") + ":" + max_time_value[1].strftime("%M")
            return (string, max_value)

        elif cumulative == True:
            return self.total(satlist_url, start_time, duration, sample_interval, location)

        """
                print(start_time)
        #Loading list of satellites
        satellites = load.tle(satlist_url)

        #Getting current time
        self.t = self.ts.now()
        print(self.t.utc_jpl())

        #Iterating over list of satellites to determine if they are over or below the horizon
        print(satellites)
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
        """

        self.t = 0
        # return (start_time, ["ISS (ZARYA)", "COSMOS-123"])

    def max(self, satlist_url='http://celestrak.com/NORAD/elements/visual.txt',
    start_time=datetime.now(), duration=60, sample_interval=1, location=(-37.910496,145.134021)):
        """
        calculates the maximum number of satellites visible at a single moment within an interval of time
        @param satlist_url: the website where we get the list of satellites
        @param start_time: the time where we want to start measure the number of satellites visible
        @param duration: the duration during which we want to measure the number of satellites visible
        @sample_interval: the intervals of time during which we will measure the number of visible satellites
        @location: the user's location
        @return: a tuple (time interval, max_number_of_satellites)
        """
        #Loading list of satellites
        satellites = load.tle(satlist_url)

        List = []
        UTC_ZONE = timezone('UTC')
        for j in range(0, duration, sample_interval):
            count = 0  # Resetting count after each iteration
            # Getting time we want to calculate
            self.t = start_time + timedelta(minutes = j)
            e = UTC_ZONE.localize(self.t)
            self.t = self.ts.utc(e)

            for i in satellites:
                if isinstance(i, str):
                    continue

                satellite = satellites[i]
                bluffton = Topos(location[0], location[1])
                difference = satellite - bluffton
                topocentric = difference.at(self.t)

                alt, az, distance = topocentric.altaz()

                if alt.degrees > 0:
                    count += 1
            end_time = start_time + timedelta(minutes = duration)
            string = ""
            string = string + start_time.strftime("%H") + ":" + start_time.strftime("%M") + "," + end_time.strftime("%H") + ":" + end_time.strftime("%M")
            List.append((string,count))
        return max(List, key = lambda item:item[1])

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
        @return: a tuple (time interval, total number of distinct satellites)
        """
        satellites = load.tle(satlist_url)

        List = []
        UTC_ZONE = timezone('UTC')
        for j in range(0, duration, sample_interval):
            # Getting time we want to calculate
            self.t = start_time + timedelta(minutes=j)
            e = UTC_ZONE.localize(self.t)
            self.t = self.ts.utc(e)

            for i in satellites:
                if isinstance(i, str):
                    continue

                satellite = satellites[i]
                bluffton = Topos(location[0], location[1])
                difference = satellite - bluffton
                topocentric = difference.at(self.t)

                alt, az, distance = topocentric.altaz()

                if alt.degrees > 0 and satellite not in List:
                    List.append(satellite)
        self.t = 0
        end_time = start_time + timedelta(minutes=duration)
        string = ""
        string = string + start_time.strftime("%H") + ":" + start_time.strftime("%M") + "," + end_time.strftime("%H") + ":" +  end_time.strftime("%M")
        return (string,len(List))


Testing = Scheduler()
# maxTest = Testing.max(satlist_url='http://celestrak.com/NORAD/elements/visual.txt',
#     start_time=datetime.now(), duration=60, sample_interval=1, location=(-37.910496,145.134021))
# print(maxTest[0], maxTest[1])
#
# totalTest = Testing.total(satlist_url='http://celestrak.com/NORAD/elements/visual.txt',
#     start_time=datetime.now(), duration=60, sample_interval=1, location=(-37.910496,145.134021))
# print(totalTest[0], totalTest[1])


findTest = Testing.find_time(satlist_url='http://celestrak.com/NORAD/elements/visual.txt',
start_time=datetime.now(), n_windows=5, duration=60, sample_interval=1, cumulative=False,
location=(-37.910496,145.134021))
print(findTest)