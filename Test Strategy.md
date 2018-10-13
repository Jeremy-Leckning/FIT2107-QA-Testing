## Test Strategy

#### Scope
Scheduler is a program coded in Python that provides information for the user about the best time interval to conduct satellite spotting. This is done by requesting information from the skyfield library which contains a list of satellites before determining which ones are visible at the specified time. A class is used to define all the methods used for the module scheduler.py and the main methods to be tested are:
* prompt
* find_time
* max
* total

#### Test Approach
The main level of testing for this test strategy will be unit testing as well as some minor mocking. A coverage tool will be used to check for coverage. Test cases will be designed and improved in a way that high coverage can be achieved. Assertions will be used to ensure that methods return values of the right typing (e.g. int, list...). As for the arguments inputted, the program is expected to raise an IllegalArgumentException when an invalid argument is used. To test for this, a range of invalid arguments will be inputted into find_time to test if an exception occurs. Unittest allows the testers to check if an exception is thrown as expected using with self.assertRaises().

#### Testing Environment
The program is being written in Python 3.6 and will be tested using Windows 10 OS. Since python is cross platform, the tests will also be able to operate on other operating systems such as linux. 

#### Testing Tools
Python has an inbuilt testing library called PyUnit which can be used to design unit tests for each of the methods. A new module schedulerTest.py will be created which will contain the test class created by subclassing unittest.TestCase. The class will contain the following test methods:
* setUp
* test_findTime
* test_max
* test_total 
* test_exceptionthrown

To test for coverage, there is a library available online which can be used to check for branch and statement coverage.

#### Mocking
The program relies on the library provided by skyfield. To test the program without the need to rely on external environment, Python’s unittest library contains a mock object which can be used to create attributes and methods. Return values can be specified to each mock object and they can be accessed when called. Details of how they have been used are also available if needed. To replace the external environment of the skyfield library, a mock will be created to represent the list of satellites along with their information imported from the library. This is done so that all testing can be done locally.

#### Continuous Integration
After creating the unit test module containing unit testing for the main methods, instead of running the test locally, gitlab’s CI can be used. A .gitlab-ci.yml file is used to set up the continuous integration. After setting everything up, everytime the module is pushed onto git, the test file will run and a feedback will be provided in the console to report whether the test has succeeded or failed. 

#### Roles
Since this project is a pairwork, both are expected to play the role of developer and tester by coding up the actual functionality of the program as well as writing up test cases that complements the main code.

