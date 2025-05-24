import pandas as pd
class Attractivity:
    def RateWeather():
        pass
    

class WMOrating(Attractivity):
    def __init__(self, rating):
        self.rating = rating

    def __str__(self):
        return f"WMOrating(rating={self.rating})"

    def __repr__(self):
        return self.__str__()

    def __eq__(self, other):
        if isinstance(other, WMOrating):
            return self.rating == other.rating
        return False
    def RateWeather(dataframe)->float:

        return dataframe['weather_code'].mean()
        
