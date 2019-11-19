import nvector as nv

#uses the positions of the prongs and pallet to calculate where a shot goes. Returns the 
#furthest point the pellet reaches
def shoot(prong1, prong2, pellet):

	#convert and calculate the middle of the sling
	nv_pellet = tuple2nvLocation(pellet)
	nv_midpoint = getMidpoint(prong1, prong2)

	#direction of shot
	azimuth = nv_pellet.delta_to(nv_midpoint).azimuth_deg[0]

	#use the distance between the players as shooting distance
	distance = triangle_perimeter(prong1, prong2, pellet)

	#calculate the destination of the shot
	endpoint, azi = nv_pellet.displace(distance=distance, azimuth=azimuth, degrees=True)

	return endpoint.latlon_deg[:2]

#checks if a shot hit the target given the location of the target, the starting position of the pellet and 
#the destination of the shot. returns true of the target was hit
def targetHit(pellet, shot_destination, target):
	#conversion
	nv_target = tuple2nvLocation(target, False)
	nv_pellet = tuple2nvLocation(pellet, False)
	nv_shot_destination = tuple2nvLocation(shot_destination, False)

	#is the shot far enough?
	if nv_pellet.distance_and_azimuth(nv_target) < nv_pellet.distance_and_azimuth(nv_shot_destination):
		#path from pellet to shoot destination
		path = nv.GeoPath(nv_pellet, nv_shot_destination)
		#target distance to path
		target_offset = path.cross_track_distance(nv_target).ravel()
		#check if shot within tolerance
		if abs(target_offset) < 10:
			return True
	return False


#returnes the geodetic midpoint between two Vertices containing coordinates
def getMidpoint(location1, location2):

    # see http://nvector.readthedocs.org/en/latest/src/overview.html?highlight=midpoint#description    
    nv_location1 = tuple2nvVector(location1)
    nv_location2 = tuple2nvVector(location2)
    path = nv.GeoPath(nv_location1, nv_location2)    
    #halfway = 0.5
    nv_midpoint = path.interpolate(0.5).to_geo_point()
    mid_lat, mid_lon = nv_midpoint.latlon_deg[:2]
    
    midpoint = (mid_lat[0], mid_lon[0])

    return nv_midpoint

#gives the sum of the distance between the three locations
def triangle_perimeter(location1, location2, location3):
	nv_location1 = tuple2nvLocation(location1)
	nv_location2 = tuple2nvLocation(location2)
	nv_location3 = tuple2nvLocation(location3)

	a = nv_location1.distance_and_azimuth(nv_location2)
	b = nv_location2.distance_and_azimuth(nv_location3)
	c = nv_location3.distance_and_azimuth(nv_location1)

	return a[0]+b[0]+c[0]


def tuple2nvLocation(location, ellipsoid=True):
	#print ("TUPLE2NVLOCATION" + location + "LOCATION[0]" + location[0])
	if ellipsoid:
		frame = nv.FrameE(name='WGS84')
	else:
		frame = nv.FrameE(a=6371e3, f=0)
	return frame.GeoPoint(location[0], location[1], degrees=True)

def tuple2nvVector(location, ellipsoid=True):
	if ellipsoid:
		frame = nv.FrameE(name='WGS84')
	else:
		frame = nv.FrameE(a=6371e3, f=0)
	return frame.GeoPoint(location[0], location[1], degrees=True).to_nvector()


target = (60.196958, 24.774768)
pellet = (60.194954, 24.780931)
shot_destination = shoot((60.195157, 24.777605), (60.196277, 24.779440), pellet)
print(shot_destination)

target_hit = targetHit(pellet, shot_destination, target)
print(target_hit)