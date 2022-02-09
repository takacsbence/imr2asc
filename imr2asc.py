#!/usr/bin/env python3
# -*- coding: utf-8 -*-
""" read binary novatel imr file and convert it into ascii
    
    imr file structure : https://docs.novatel.com/Waypoint/Content/Data_Formats/IMR_File.htm
"""

import sys
import struct
        
def convert_header(data):
    struct_fmt = '=8sbdiidddiid32si32s12s?iii354s' # 
    struct_len = struct.calcsize(struct_fmt)
    struct_unpack = struct.Struct(struct_fmt).unpack_from
    header = struct_unpack(data)

    return header

def convert_data(data, header):

    DeltaTheta = header[3]
    DeltaVelocity = header[4]
    DataRateHz = header[5]
    GyroScaleFactor = header[6]
    AccelScaleFactor = header[7]
    UtcOrGpsTime = header[8]
    RcvTimeOrCorrTime = header[9]
    TimeTagBias = header[10]
    Create = header[14] #type is "time_type", figure out what doest it mean

    #print(RcvTimeOrCorrTime)

    struct_fmt = '=diiiiii'
    struct_len = struct.calcsize(struct_fmt)
    struct_unpack = struct.Struct(struct_fmt).unpack_from

    s = struct_unpack(data)
    time = float(s[0]) - TimeTagBias / 1000
    gyro = []
    accel = []
    if DeltaTheta == 0: #todo:else
        for i in range(3):
            gyro.append(float(s[i+1]) * GyroScaleFactor)
    if DeltaVelocity == 0: #todo:else
        for i in range(3):
            accel.append(float(s[i+4]) * AccelScaleFactor)
    return time, gyro, accel

#input file as first argument
if len(sys.argv) > 1:
    finp = sys.argv[1]
else:
    print("missing input file")
    print("correct use: python", sys.argv[0], "input_file")
    sys.exit()

#open input file
try:
    filei = open(finp, 'rb')
except IOError:
    print("Could not open file:", finp)
    sys.exit()

#output file
foutp = finp[:-4] + '.asc'
try:
    fileo = open(foutp, 'w')
except IOError:
    print("Could not open file:", foutp)
    sys.exit()

#read input file
with filei:
    data = filei.read(512)   #read header 512 bytes
    header = convert_header(data)

    print("Time              Gyro_X     Gyro_Y     Gyro_Z    Accel_X    Accel_Y    Accel_Z", file=fileo)
    nr = 0 #nr if records
    while data and nr < 10:
        data = filei.read(32)   #read data
        nr += 1
        if not data: break
        
        time, gyro, accel = convert_data(data, header)
        print("{:.6f} {:10.5f} {:10.5f} {:10.5f} {:10.5f} {:10.5f} {:10.5f}".format(time, gyro[0], gyro[1], gyro[2], accel[0], accel[1], accel[2]), file=fileo)

print("{:d} data read from {:s} and written to {:s}".format(nr, finp, foutp))