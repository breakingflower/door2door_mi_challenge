###################################################################
# Script Name	 : "TEST_STATICDATAREADER.PY"                                                                                         
# Description	 : Tests for the utilities/staticdatareader.py file                                                                                
# Args           :                                                                                           
# Author       	 : Floris Remmen                                              
# Email          : floris.remmen@gmail.com 
# Date           : "28 September 2020"                                     
###################################################################

import unittest
from utilities.staticdatareader import StaticDataReader

class TestStaticDataReader(unittest.TestCase): 
    """
    Testcase for the Visualiser Class
    """
    @classmethod
    def setUpClass(self): 
        """
        Sets up a case where good filenames are given and a case
        where bad filenames are given.
        """

        self.static_data_good = StaticDataReader(
            'data/berlin_bounds.poly', 
            'data/berlin_stops.geojson'
        )
        self.static_data_bad = StaticDataReader(
            'somerandomfile.jpeg', 
            'someotherfile.pngx'
        )
        
    def setUp(self): 
        pass

    def test_read_berlin_bounds(self): 
        """
        Tests output of _read_berlin_bounds().
        The instance where the files exist is not empty
        The ones where bogus filenames are used should be empty.
        """
        self.assertFalse(self.static_data_good.berlin_bounds.empty)
        self.assertTrue(self.static_data_bad.berlin_bounds.empty)

    def test_read_berlin_stops(self): 
        """
        Similar to test_read_berlin_bounds.
        Tests output of _read_berlin_bounds().
        The instance where the files exist is not empty
        The ones where bogus filenames are used should be empty.
        """
        self.assertFalse(self.static_data_good.berlin_stops.empty)
        self.assertTrue(self.static_data_bad.berlin_stops.empty)

    def tearDown(self): 
        pass

    if __name__ == "__main__":
        unittest.main()