from pyproj import Proj, transform

class BoundingBox: 
    """
    Class for bounding box. Essentially a property class: center, lats, lons, ...
    """

    def __init__(self, bounding_box: tuple): 
        
        # bounding box is x1, y1, x2, y2
        self.bounding_box = [float(val) if type(val) is not str else float("NaN") for val in bounding_box]
       
    def to_crs(self, epsg=3857) -> tuple: 
        """
        Projects the bounding box coordinates to a new coordinate system. 
        Needed for plotting onto a web mercator map, e.g. contextily.
        :rtype tuple
        """

        in_proj = Proj(init='epsg:4326')
        out_proj = Proj(init=f'epsg:{epsg}')

        x1_proj, y1_proj = transform(in_proj, out_proj, self.bounding_box[0], self.bounding_box[1])
        x2_proj, y2_proj = transform(in_proj, out_proj, self.bounding_box[2], self.bounding_box[3])

        return (x1_proj, y1_proj, x2_proj, y2_proj)

    @property
    def center(self) -> tuple: 
        """
        Returns a tuple with the center of the bounding box, calculated by averaging lat/lon coordinates.
        eg (y0 + y1) / 2 , (x0 + x1) / 2
        :rtype tuple
        """
        return (self.bounding_box[1] + self.bounding_box[3]) / 2, (self.bounding_box[0] + self.bounding_box[2]) / 2
        
    @property
    def lats(self) -> list: 
        """
        Returns list of four latitude coordinates
        :rtype list
        """
        return [self.bounding_box[1], self.bounding_box[3], self.bounding_box[3], self.bounding_box[1]]
    
    @property
    def lons(self) -> list:
        """
        Returns list of four longitude coordinates
        :rtype list
        """
        return [self.bounding_box[0], self.bounding_box[0], self.bounding_box[2], self.bounding_box[2]]