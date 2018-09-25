import sys
sys.path.append('../src')
from coordinate import Coordinate

def withinRange(result, actual, allowedError):
   if(abs(result - actual) <= allowedError):
      return True

   return False

def testDistance():
   coord1 = Coordinate()
   coord1.setLatitude(41.153774)
   coord1.setLongitude(-81.358218)

   coord2 = Coordinate()
   coord2.setLatitude(41.153777)
   coord2.setLongitude(-81.356356)
   
   result = coord1.distanceInMeters(coord2)
   actualDistance = 150.5 #Aquired from google maps
   allowedError = 10

   assert withinRange(result, actualDistance, allowedError)

def main():
   testDistance()
   print("test_coordinate.py passed")

if __name__ == "__main__":
   main()
