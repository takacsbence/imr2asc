# imr2asc
binary ascii conversion of novatel IMU data

imr file structure : https://docs.novatel.com/Waypoint/Content/Data_Formats/IMR_File.htm

output:

Time              Gyro_X     Gyro_Y     Gyro_Z    Accel_X    Accel_Y    Accel_Z

390039.152268   -3.19724    0.08329    0.42469   -0.38602    0.33630    9.81521

390039.154268   -2.86998    0.05710    0.48474   -0.40374    0.34184    9.81151

390039.156268   -2.53532    0.01431    0.54658   -0.41385    0.34688    9.81064


Time: gps seconds of week [s]

Gyro_[XYZ]: gyro measurements [deg/s]

Accel_[XYZ]: acceleration measurements [m/s^2]
