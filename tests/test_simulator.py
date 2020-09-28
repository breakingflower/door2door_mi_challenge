###################################################################
# Script Name	 : "TEST_SIMULATOR.PY"                                                                                         
# Description	 : Tests for the simulator/simulator.py file                                                                                
# Args           :                                                                                           
# Author       	 : Floris Remmen                                              
# Email          : floris.remmen@gmail.com 
# Date           : "28 September 2020"                                     
###################################################################

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
        """
        Test output of get_booking_distance_bins. This should return a dict with size
        len(Simulator().booking_distance_distribution)
        """
        booking_distance_bins = self.simulator.get_booking_distance_bins(self.n)
        self.assertIsInstance(booking_distance_bins, dict)
        self.assertEqual(len(booking_distance_bins), len(self.simulator.booking_distance_distribution))

    
    def test_simulate(self): 
        """
        This test asserts that the output of the simulation is a dictionary with size 3.
        This uses some distribution so defining a test is limited to output type
        """
        simulation = self.simulator.simulate(self.n)

        self.assertIsInstance(simulation, dict)
        self.assertEqual(len(simulation), 3)

    def tearDown(self): 
        pass

    if __name__ == "__main__":
        unittest.main()