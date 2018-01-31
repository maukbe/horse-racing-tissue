from position import Position

class RaceResult:
    def __init__(self, distance, position):
        self.distance = distance
        self.position = position
        
    # Distance in furlongs
    @property
    def distance(self):
        return self.__distance
        
    @distance.setter
    def distance(self, distance):
        self.__distance = distance

    
    # Race position
    @property
    def position(self):
        return self.__position
        
    @position.setter
    def position(self, position):
        self.__position = position