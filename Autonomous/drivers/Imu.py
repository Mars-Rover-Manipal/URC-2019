from geopy import distance
from Gps import current_pos
from magneto import get_imu_head
g = pyproj.Geod(ellps='WGS84')
def get_heading(endlong,endlat):
    startlat,startlong=current_pos()
    (angle, az21, dist) = g.inv(startlong, startlat, endlong, endlat)
    if angle<0:
        angle=angle+360
    return angle, dist
