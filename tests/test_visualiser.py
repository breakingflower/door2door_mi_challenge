import unittest
from visualiser.visualiser import Visualiser

from utilities.bounding_box import BoundingBox
from utilities.staticdatareader import StaticDataReader
from simulator.simulator import Simulator

import warnings

from os.path import isfile

class TestVisualiser(unittest.TestCase): 
    """
    Testcase for the Visualiser Class
    """

    @classmethod
    def setUpClass(self): 
        """
        Sets up the class. The data only has to be read in once, so this is done in the class setup method.
        """
        # TODO: Remove warn ngs filter when migrating to geopandas > 0.7.0 !
        warnings.simplefilter('ignore', category=FutureWarning)
        warnings.simplefilter('ignore', category=DeprecationWarning)

        static_data = StaticDataReader(
            'data/berlin_bounds.poly', 
            'data/berlin_stops.geojson'
        )
        bounding_box_tuple = (
            13.34014892578125, 
            52.52791908000258, 
            13.506317138671875, 
            52.562995039558004
        )
        simulator = Simulator(
            bounding_box = bounding_box_tuple
        )
        simulation_results = simulator.simulate(number_of_requests=6)

        self.visualiser = Visualiser(
            bounding_box = BoundingBox(bounding_box_tuple), 
            simulation_results = simulation_results, 
            static_data= static_data, 
            static_path = 'webapp/static'
        ) 

    def setUp(self): 
        pass

    def test_generate_overview_figure(self): 
        """
        Asserts a overview figure is generated after calling the function.
        """
        self.visualiser.generate_overview_figure()

        self.assertTrue(
            isfile(f"{self.visualiser.static_path}/{self.visualiser.id}_overview_plot.png")
        )
        
    def test_generate_closeup_figure(self): 
        """
        Asserts a closeup figure is generated after calling the function.
        """
        self.visualiser.generate_closeup_figure()

        self.assertTrue(
            isfile(f"{self.visualiser.static_path}/{self.visualiser.id}_closeup_plot.png")
        )

    def test_generate_gmap(self): 
        """
        Asserts a html map is generated after calling the function.
        """
        self.visualiser.generate_gmap()

        self.assertTrue(
            isfile(f"{self.visualiser.static_path}/{self.visualiser.id}_map.html")
        )

    def tearDown(self): 
        pass

    if __name__ == "__main__":
        unittest.main()