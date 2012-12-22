"""
a4test.py v1.0: Allows you to test Mosaic, FractalMosaic, and EnhancedMosaic
outputs.
    Copyright (C) 2011 Twine. All rights reserved.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    FITNESS FOR A PARTICULAR PURPOSE.
"""

# Set these to False if you don't want to run a certain test suite.
# If a file is missing, the program as a whole may not run, even if you aren't
# testing all files.

MOSAIC = True
FRACTAL_MOSAIC = True
ENHANCED_MOSAIC = True

# Set the min_size and threshold values to use for the tests
MIN_SIZE = 10
THRESHOLD = 60

# Set the verbosity value to be passed to the test runner, between 0 and 5.
VERBOSITY = 1

# Number of digits of time to output (including the decimal).
# Should be a non-negative integer.
TIME_ACCURACY = 8

if MOSAIC:
    from mosaic import Mosaic
if FRACTAL_MOSAIC:
    from fractal_mosaic import FractalMosaic
if ENHANCED_MOSAIC:
    from enhanced_mosaic import EnhancedMosaic
import unittest
from os.path import isfile
from time import time
import os

# Checks if a stylechecker is present, and runs it if it is.
STYLECHECK = False
if isfile('./stylecheck.py'):
    STYLECHECK = True
    import stylecheck as stylechecker
elif isfile('./stylechecker.py'):
    STYLECHECK = True
    import stylechecker
    
def test_style(filename):
    """Run the stylechecker on the file given. Return True if it passes the
       stylechecker, and False otherwise.
    """
    
    return_value = False
    stylechecker.process_options(['-v', '--count', filename])
    stylechecker.input_file(filename)
    if stylechecker.get_statistics() == []:
        print "Congrats! No style errors were detected."
        return_value = True
    stylechecker.options = None
    return return_value    
     
class fractalMosaicTestCase(unittest.TestCase):
    """Test cases for FractalMosaic."""
    
    def setUp(self):
        """Set up."""
        
        self.mosaic = FractalMosaic('./dali')
        
    def tearDown(self):
        """Clean up."""
        
        self.mosaic = None
        
    def testCreateMosaic(self):
        """Test creating a fractal mosaic."""
        
        self.mosaic.create_mosaic('./karan.jpg', MIN_SIZE, THRESHOLD)
        self.mosaic.save_as('./output_fractal.jpeg')
        
class enhancedMosaicTestCase(unittest.TestCase):
    """Test cases for EnhancedMosaic."""
    
    def setUp(self):
        """Set up."""
        
        self.mosaic = EnhancedMosaic('./dali')
        
    def tearDown(self):
        """Clean up."""
        
        self.mosaic = None
        
    def testCreateMosaic(self):
        """Test creating a fractal mosaic."""
        
        self.mosaic.create_mosaic('./karan.jpg', MIN_SIZE, THRESHOLD)
        self.mosaic.save_as('./output_enhanced.jpeg')
        
class mosaicTestCase(unittest.TestCase):
    """Test cases for EnhancedMosaic."""
    
    def setUp(self):
        """Set up."""
        
        self.mosaic = Mosaic('./dali')
        
    def tearDown(self):
        """Clean up."""
        
        self.mosaic = None
        
    def testCreateMosaic(self):
        """Test creating a fractal mosaic."""
        
        self.mosaic.create_mosaic('./karan.jpg', MIN_SIZE)
        self.mosaic.save_as('./output.jpeg')
        
def mosaic_test_suite():
    """Return a test suite for Mosaic."""
    
    return unittest.TestLoader().loadTestsFromTestCase(mosaicTestCase)

def fractal_mosaic_test_suite():
    """Return a test suite for FractalMosaic."""
    
    return unittest.TestLoader().loadTestsFromTestCase(fractalMosaicTestCase)

def enhanced_mosaic_test_suite():
    """Return a test suite for EnhancedMosaic."""
    
    return unittest.TestLoader().loadTestsFromTestCase(enhancedMosaicTestCase)

def runTestSuites(testsuites, message):
    """Take in a list of test suites and a string message to label the suites.
       Run the suites, and return a tuple containing the total number of tests
       run and failed, and the total number of errors, as well as the input
       message.
    """
    total, failed, errors = 0, 0, 0
    print ""
    print "########################"
    print "Running " + message
    print "########################"
    print ""
    start_time = time()
    for suite in testsuites:
        result = runner.run(suite)
        total += result.testsRun
        failed += len(result.failures)
        errors += len(result.errors)
    time_elapsed = time() - start_time
    return (total, failed, errors, message, time_elapsed)

def display_results(results):
    """Take in a list of tuples containing the number of tests, failures, and
       errors in each test suite, and also containing a string describing
       that test suite. Display the test results using print.
    """
    
    total, failed, errors, total_time = 0, 0, 0, 0
    print ""
    for result in results:
        total += result[0]
        failed += result[1]
        errors += result[2]
        total_time += result[4]
        if result[1] + result[2] > 0:
            print (result[3] + " FAILED with " + str(result[1]) + "/" +
            str(result[0]) + " failures and " + str(result[2]) + "/" +
            str(result[0]) + " errors.")
        else:
            print ("All " + str(result[0]) + " cases from " + result[3] +
            " passed in " + str(result[4])[:TIME_ACCURACY] + " seconds.")
    print ""
    if failed + errors == 0:
        print "Congratulations! All tests passed."
    else:
        print "Sorry! Not all tests were passed."
    print ("Completed " + str(total) + " tests in " +
           str(total_time)[:TIME_ACCURACY] +  " seconds with " + str(failed) +
           " failures and " + str(errors) + " errors.")

def select_verbosity():
    """Ask for a user-defined integer verbosity level between 0 and 5, and
       return that verbosity, or default to 1.
    """
    
    print "Select verbosity level from 0 to 5 (1 default): ",
    choice = raw_input()
    if choice.isdigit() and int(choice) < 6:
        return int(choice)
    else:
        return 1
    
if __name__ == '__main__':
    runner = unittest.TextTestRunner(verbosity=VERBOSITY)
    mosaictestsuites = [mosaic_test_suite()]
    fractalmosaictestsuites = [fractal_mosaic_test_suite()]
    enhancedmosaictestsuites = [enhanced_mosaic_test_suite()]
    if STYLECHECK:
        print "\nRunning style checker."
        S = []
        if MOSAIC:
            S.append('./mosaic.py')
        if FRACTAL_MOSAIC:
            S.append('./fractal_mosaic.py')
        if ENHANCED_MOSAIC:
            S.append('./enhanced_mosaic.py')
        style_pass = all([test_style(module) for module in S])
    R = []
    # rpn_list_eval test cases
    if MOSAIC:
        R.append(runTestSuites(mosaictestsuites,
                               "Mosaic test suites"))
    # test_tree_to_rpn_list test cases
    if FRACTAL_MOSAIC:
        R.append(runTestSuites(fractalmosaictestsuites,
                               "FractalMosaic test suites"))
    if ENHANCED_MOSAIC:
        R.append(runTestSuites(enhancedmosaictestsuites,
                               "EnhancedMosaic test suites"))
    # Display results
    display_results(R)
    if STYLECHECK:
        if style_pass:
            print "All modules passed the style checker."
        else:
            print "ATTENTION: Some modules failed the style checker. See the start of the output."
