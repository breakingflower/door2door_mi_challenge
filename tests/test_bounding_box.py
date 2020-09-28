###################################################################
# Script Name	 : "TEST_BOUNDING_BOX.PY"                                                                                         
# Description	 : Tests for the utilities/bounding_box.py file.                                                                                
# Args           :                                                                                           
# Author       	 : Floris Remmen                                              
# Email          : floris.remmen@gmail.com 
# Date           : "28 September 2020"                                     
###################################################################

import unittest
from utilities.bounding_box import BoundingBox
import math

import warnings

class TestBoundingBox(unittest.TestCase):
    """
    Test case for the BoundingBox class. 
    """
    
    def setUp(self): 
        """
        Sets up the test cases for the BoundingBox class.
        FutureWarnings and DeprecationWarnings are ignored. This is because of the dependencies in the simulator class
        """
        # TODO: Remove warnings filter when migrating to geopandas > 0.7.0 !
        warnings.simplefilter('ignore', category=FutureWarning)
        warnings.simplefilter('ignore', category=DeprecationWarning)

        self.bad_bbox = BoundingBox(("a", "b", 23.4, 34.2))
        self.good_bbox = BoundingBox(
            (
                13.34014892578125, 
                52.52791908000258, 
                13.506317138671875, 
                52.562995039558004
            )
        )

    def test_to_crs(self): 
        """
        Tests the to_crs function. Should return ValueError and TypeError for bad_bbox.
        Good values should be equal
        """
        self.assertRaises((ValueError, TypeError), self.bad_bbox.to_crs()) 
        self.assertEqual(self.good_bbox.to_crs(), ((1485018.5855244042, 6896148.6918886015, 1503516.3463694167, 6902569.402264554)))
    
    def test_lats(self):
        """
        Tests the lats property. Should return TypeError for bad_bbox.
        Good values should be equal. 
        """
        self.assertRaises(TypeError, self.bad_bbox.lats) 
        self.assertListEqual(self.good_bbox.lats, [52.52791908000258, 52.562995039558004, 52.562995039558004, 52.52791908000258])
    
    def test_lons(self): 
        """
        Tests the lons property. Should return TypeError for bad_bbox.
        Good values should be equal. 
        """
        self.assertRaises(TypeError, self.bad_bbox.lons) 
        self.assertListEqual(self.good_bbox.lons, [13.34014892578125, 13.34014892578125, 13.506317138671875, 13.506317138671875])
    
    def tearDown(self): 
        del self

    if __name__ == "__main__":
        unittest.main()