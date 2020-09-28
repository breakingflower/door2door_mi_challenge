import unittest
from simulator.simulator import Simulator

import warnings

class TestSimulator(unittest.TestCase): 
    """
    Testcase for the Simulator Class
    """

    def setUp(self): 

        self.simulator = Simulator(
            bounding_box = (
                13.34014892578125, 
                52.52791908000258, 
                13.506317138671875, 
                52.562995039558004
            )
        )
        self.n = 6

    def test_get_booking_distance_bins(self): 
        self.assertIsInstance(self.simulator.get_booking_distance_bins(self.n), dict)
    
    def test_simulate(self): 
        """
        This uses some distribution so defining a test is limited to output type
        """
        self.assertIsInstance(self.simulator.simulate(self.n), dict)

    def tearDown(self): 
        pass

    if __name__ == "__main__":
        unittest.main()