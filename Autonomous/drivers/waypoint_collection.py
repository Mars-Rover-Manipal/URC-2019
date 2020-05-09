import json
from drivers.gps.gpsNmea import GPS
gps = GPS("/dev/ttyS0")
waypoints = []

choice = input("a to add a waypoint, q to quit\n")
while choice == "a":
	waypoints.append(gps.location())
	print("Waypoints: ", waypoints)
	choice = input("a to add another waypoint, q to quit")

with open('waypoints.json','wb') as waypointfile:
	json.dump(waypoints, waypointfile)
	
print ("Waypoints saved")