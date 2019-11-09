import csv
from math import sin, cos, sqrt, atan2, radians

# distance.py returns the
# what is location?

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

def return_nearest_location_coordinates(my_location):
	with open('locations.csv', encoding='utf-8-sig') as f:
		data=[tuple(line) for line in csv.reader(f)]

	shortestDistance = 5000
	#coordinates for best location
	result = None

	for location in data:
		cur_distance = haversine(my_location, location)
		# print("distance is " + str(distance))
		if cur_distance <= shortestDistance:
			shortestDistance = cur_distance
			result = location

	return result