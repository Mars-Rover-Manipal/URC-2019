import smbus
import time
import math

bus = smbus.SMBus(1)
pi = 3.14159265358979
bus.write_byte_data(0x6B, 0x20, 0x0F)
bus.write_byte_data(0x6B, 0x23, 0x30)
time.sleep(0.5)
data0 = bus.read_byte_data(0x6B, 0x28)
data1 = bus.read_byte_data(0x6B, 0x29)
data0 = bus.read_byte_data(0x6B, 0x2A)
data1 = bus.read_byte_data(0x6B, 0x2B)
data0 = bus.read_byte_data(0x6B, 0x2C)
data1 = bus.read_byte_data(0x6B, 0x2D)
bus.write_byte_data(0x1D, 0x20, 0x67)
bus.write_byte_data(0x1D, 0x21, 0x20)
bus.write_byte_data(0x1D, 0x24, 0x70)
bus.write_byte_data(0x1D, 0x25, 0x60)
bus.write_byte_data(0x1D, 0x26, 0x00)
time.sleep(0.5)
data0 = bus.read_byte_data(0x1D, 0x28)
data1 = bus.read_byte_data(0x1D, 0x29)
data0 = bus.read_byte_data(0x1D, 0x2A)
data1 = bus.read_byte_data(0x1D, 0x2B)
data0 = bus.read_byte_data(0x1D, 0x2C)
data1 = bus.read_byte_data(0x1D, 0x2D)
def get_imu_head():
        while True:
                data0 = bus.read_byte_data(0x1D, 0x08)
                data1 = bus.read_byte_data(0x1D, 0x09)
                xMag = data1 * 256 + data0
                if xMag > 32767 :
                        xMag -= 65536
                data0 = bus.read_byte_data(0x1D, 0x0A)
                data1 = bus.read_byte_data(0x1D, 0x0B)
                yMag = data1 * 256 + data0
                if yMag > 32767 :
                        yMag -= 65536
                data0 = bus.read_byte_data(0x1D, 0x0C)
                data1 = bus.read_byte_data(0x1D, 0x0D)
                zMag = data1 * 256 + data0
                if zMag > 32767 :
                        zMag -= 65536
                h= math.atan2(-yMag,xMag)
                if(h > 2*pi):
                        h=h-2*pi
                if(h<0):
                        h=h+2*pi
                ha=int(h* 180/pi)
                ha = ha+7
                if ha>359:
                        ha = ha-360
                return ha
 