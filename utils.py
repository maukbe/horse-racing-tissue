# Utility functions for conversions etc.
from position import Position

KILOS_IN_POUNDS = 2.204
POUNDS_IN_STONE = 14

# Take a string of form WON/X or Y/X ad return an enum of whether it placed
# @result String of the result
# @return Position enum
def parse_result(resultString):
    result = resultString.split("/")
    if "Won" in result[0]:
        return Position.WON
    elif result[0] == "PU" or result[0] == "F" or "R" in result[0]:
        return Position.DIDNT_PLACE
    else:
        return did_place(int(result[0]), int(result[1]))
            
def did_place(position, runners):
    if runners >= 16:
        if position <= 4:
            return Position.PLACED
        else:
            return Position.DIDNT_PLACE
    elif runners <= 15 and runners >= 8:
        if position <= 3:
             return Position.PLACED
        else:
            return Position.DIDNT_PLACE
    elif runners <=7 and runners >= 5:
        if position <= 2:
             return Position.PLACED
        else:
            return Position.DIDNT_PLACE
    else:
        return Position.DIDNT_PLACE
        

# Convert weight in pounds to kilos
# @weightPounds Weight in stones and pounds 10-4
# @return       Weight in kilos
def poundsToKilos(weightPounds):
    return int(weightPounds) / KILOS_IN_POUNDS
    
# Extract weight in kilos from string of form 11-3
# @weightString Weight string
# @return       Integer weight in kilos
def parseWeight(weightString):
    poundsKilos = weightString.split("-")
    return POUNDS_IN_STONE*int(poundsKilos[0]) + int(poundsKilos[1])
    
# Get distance in furlongs from string of form 1m 3F 123yds
# @distance_string Distance string
# @return           Distance in furlongs
def parse_distance(distance_string):
    distance = distance_string.split(" ")
    miles =  int(distance[0].split("m")[0])
    furlongs = 0
    if len(distance) > 1:
        furlongs = int(distance[1].split("f")[0])
    return 8*miles + furlongs

    
    
    
    