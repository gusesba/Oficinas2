from mpu6050 import mpu6050
import time

class SensorGiroscopioAcel:
    def __init__(self):
        self.mpu = mpu6050(0x68)
    def readData(self):
        print("Temp : "+str(self.mpu.get_temp()))
        print()

        accel_data = self.mpu.get_accel_data()
        print("Acc X : "+str(accel_data['x']))
        print("Acc Y : "+str(accel_data['y']))
        print("Acc Z : "+str(accel_data['z']))
        print()

        gyro_data = self.mpu.get_gyro_data()
        print("Gyro X : "+str(gyro_data['x']))
        print("Gyro Y : "+str(gyro_data['y']))
        print("Gyro Z : "+str(gyro_data['z']))
        print()
        print("-------------------------------")
