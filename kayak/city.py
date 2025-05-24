class PointOfInterest:
    def __init__(self, id:int, name:str, latitude:float, longitude:float):
        """Initialize a Point of Interest.  
        Args:
            id (int): Unique identifier for the point of interest from OSM
            name (str): Name of the point of interest.
            latitude (float): Latitude coordinate of the point of interest.
            longitude (float): Longitude coordinate of the point of interest.
        """
        self.id = id    # unique identifier for the point of interest from OSM
        self.name = name # name of the point of interest
        self.lat = latitude # latitude of the point of interest
        self.lon = longitude    # longitude of the point of interest
        self.nice=100.0 # attractive score, default is 100.0
        self.hotels=[]  # list of hotels nearby, default is empty list
    def __repr__(self):
        """Representation of the Point of Interest."""
        return f"PointOfInterest(id={self.id}, name='{self.name}', lat={self.lat}, lon={self.lon})"
    def __str__(self):
        """String representation of the Point of Interest."""
        return f"{self.name} ({self.lat}, {self.lon})"
