import csv
from math import sin, cos, sqrt, atan2, radians

def haversine(my_location, location):
	# approximate radius of earth in km
	R = 6373.0

	lat1 = radians(my_location[0])
	lon1 = radians(my_location[1])
	lat2 = radians(float(location[0]))
	lon2 = radians(float(location[1]))

	dlon = lon2 - lon1
	dlat = lat2 - lat1

	a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
	c = 2 * atan2(sqrt(a), sqrt(1 - a))

	distance = R * c
	return distance

def return_nearest_location(my_location):
	with open('locations.csv', encoding='utf-8-sig') as f:
		data=[tuple(line) for line in csv.reader(f)]

	shortestRoute = 5000
	#coordinates for best location
	best_location = None

	for location in data:
		distance = haversine(my_location, location)
		# print("distance is " + str(distance))
		if distance <= shortestRoute:
			shortestRoute = distance
			best_location = location

	# print("shortestRoute " + str(shortestRoute))
	# print("best location is " + str(best_location))
	return best_location