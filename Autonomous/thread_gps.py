import threading
import time
from gps3 import gps3
latitude=0
longitude=0
gps_socket = gps3.GPSDSocket()
data_stream = gps3.DataStream()
gps_socket.connect()
gps_socket.watch()
class GPS(object):

    def __init__(self):
    
        thread = threading.Thread(target=self.run, args=())
        thread.daemon = True                            
        thread.start()                                  

    def run(self):
        while True:
            global latitude,longitude
            print('here1')
            for new_data in gps_socket:
                if new_data:
                    data_stream.unpack(new_data)
                    global latitude,longitude
                    slatitude =  data_stream.TPV['lat']
                    slongitude =  data_stream.TPV['lon']
                    if type(slongitude) is type('sdas') or type(slatitude) is type('sdas'):
                        continue
                    else:
                        latitude=slatitude
                        longitude=slongitude     


example = GPS()
start=time.time()
while time.time()-start<10:
    print(latitude,longitude)
