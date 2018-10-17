## Test Strategy

### Scope
**Scheduler** is a program coded in Python that provides information for the user about the best time interval to conduct satellite spotting. This is done by requesting information from the Skyfield library which contains a list of satellites before determining which ones are visible at the specified time. The class Scheduler is used to define all the methods used for the module scheduler.py and the main methods to be tested are:
* load_satellites
* find_time
* satellite_visibility
* max
* total

Another class named **IllegalArgumentException** is used to handle all the exceptions raised when running the code. 
### Test Approach
The goal of creating test cases is to test for the functionality of the Scheduler module and the main level of testing for this test strategy will be **Unit Testing**. To test the code without relying on external factors, some simple **Mocking** will be done.

Firstly, test cases are designed using a subdomain blackbox technique such as **Equivalence Partitioning**. An example of an equivalence class would be Valid/Invalid inputs. The main goal of these test cases is to achieve a high coverage, mainly **Branch and Statement Coverage**. To track the amount of coverage that the code has achieved, a Python coverage tool can be used. If the test cases designed before is found to not have met the targetted coverage, an **inverse approach** can be used where more test cases can be designed and improved in such a way that a higher coverage can be achieved. 

Moving on, **Assertions** will be used to ensure that methods return values of the right typing (e.g. int, list, etc...). As for the arguments inputted, the program is expected to raise an IllegalArgumentException when an invalid argument is used. To test for this, a range of invalid arguments will be inputted into find_time to test if an exception occurs. Unittest allows the testers to check if an exception is thrown as expected using with **self.assertRaises()**.

### Testing Environment
The program is being written in **Python 3.6** and will be tested using the Operating System **Windows 10**. Since python is cross platform, the tests will also be able to operate on other operating systems such as linux. 

### Testing Tools
###### Unit tests
Python has an inbuilt testing library called **PyUnit** which can be used to design unit tests for each of the methods. A new module schedulerTest.py will be created which will contain the test class SchedulerTest created by subclassing **unittest.TestCase**. The class will contain the following test methods:
* setUp
* test_max
* test_total 
* test_findTime_cumulative_false
* test_findTime_cumulative_true
* test_load_satellites
* test_exceptionthrown

When the class is called, all of the methods inside it starting with a **test_** will be called. It works in such a way that it will keep running even if one of the test failed beforehand. At the end, it will report whether the test was succesful or whether it failed along with information such as what made it fail.
###### Mocking
The program relies on the library provided by skyfield. To test the program without the need to rely on external environment, Python’s unittest library contains a mock object which can be used to create attributes and methods. Return values can be specified to each mock object and they can be accessed when called. Details of how they have been used are also available if needed. 

The strategy is to mock out all of the functionality relying on the Skyfield API and only test functionality of the module. Codes which relies on the api are placed inside a separate function (load_satellites and satellite_visibility). After that is done, the return values for them are set manually to contain dummy data that can be used to test max() and total(). Since find_time() relies on return values of max() and total(), when testing for find_time(), the values of max() and total() can also be mocked. To change the return values of the functions in every iteration, Python's MagicMock() has a functionality called **side_effect** which can be used. In order for the mocks created to have the same attributes and methods as the real object, speccing should be used so an AttributeError would be raised if the method called in MagicMock() does not exist in the real object.

###### Coverage
Python has a **Coverage tool** which after running and analyzing the Python program, it can show the amount of **branch** and **statement** coverage achieved by the code. Besides that, it can also inform the user about which sections of the code that are not being ran. This information is useful since it can be used to generate new test cases specifically designed to cover the lines of code which were omitted in testing, which in turn will increase the coverage and result in a more complete testing.

### Continuous Integration
After creating the unit test module containing unit testing for the main methods, instead of running the test locally, gitlab’s CI can be used. A **.gitlab-ci.yml** file is used to set up the continuous integration. Libraries imported should be installed in the file using pip. After setting everything up, everytime the module is pushed onto git, the test file will run and a feedback will be provided in the console to report whether the test has succeeded or failed. 

### Roles
Since this project is a pairwork, both are expected to play the role of developer and tester by coding up the actual functionality of the program as well as writing up test cases that complements the main code.

### Test Strategy to Test Cases


