import unittest
from utilities.bounding_box import BoundingBox

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

        self.false_bbox = BoundingBox(("a", "b", 23.4, 34.2))
        self.good_bbox = BoundingBox(
            (
                13.34014892578125, 
                52.52791908000258, 
                13.506317138671875, 
                52.562995039558004
            )
        )

    def test_to_crs(self): 
        self.assertRaises((ValueError, TypeError), self.false_bbox.to_crs()) 
        self.assertEqual(self.good_bbox.to_crs(), ((1485018.5855244042, 6896148.6918886015, 1503516.3463694167, 6902569.402264554)))
    
    def test_lats(self):
        self.assertRaises(TypeError, self.false_bbox.lats)
        self.assertEqual(self.good_bbox.lats, [52.52791908000258, 52.562995039558004, 52.562995039558004, 52.52791908000258])
    
    def test_lons(self): 
        self.assertRaises(TypeError, self.false_bbox.lons)
        self.assertEqual(self.good_bbox.lons, [13.34014892578125, 13.34014892578125, 13.506317138671875, 13.506317138671875])
    
    def tearDown(self): 
        del self

    if __name__ == "__main__":
        unittest.main()